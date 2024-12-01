import argparse
import ollama
import os
import requests
import json
import re
import time
import logging
from Gen_DataSet.config.config import CONFIG
from Gen_DataSet.util.util_dir import add_history,add_record,add_result,update_record,load_history,load_record,load_result,get_history_str_by_keyword
from Gen_DataSet.chat.chat import chat_ollama_stream_post



#todo
#1.总结时将适量的历史输出也输入进去 使得输出的背景不会频繁变化 （一本书一个txt文件，或者一个文件夹一本书  避免历史信息混杂，输出错乱）
#2.意外中断后，重新运行时，从上次中断的地方开始，而不是从头开始   （记录已处理的文件，从上次中断的地方开始 一个文件夹一本书）
#3.小说分章功能 将一个txt文件分成多个txt文件，每个txt文件一个章节

class Segment_Plot_Ollama_Dir:
    def __init__(self):

        self.output_dir = CONFIG.get_func_dir('summary_plot')

        self.history_path,self.result_path,self.record_path=CONFIG.get_path_with_prefix(self.output_dir,False)


        self.record={
            "files": 0,
            "segments": 0
        }
        self.history=[]



    # 定义数据预处理函数
    def preprocess_data(self,corpus_path="input", output_dir="output", n=500, batch_size=100): 

        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        output_json_path = os.path.join(output_dir, "2corpus_processed.json")
        log_file_path = os.path.join(output_dir, '2process_log.log')

        data = []
        file_count = 0
        max_files = 205027

        # 设置日志配置
        logging.basicConfig(
            filename=log_file_path,  # 日志文件名
            level=logging.INFO,       # 日志级别
            format='%(asctime)s - %(message)s',  # 日志格式
            filemode='a'              # 追加模式
        )

    

        start_time = time.time()
        # 遍历语料库路径下的所有txt文件
        chapter_num=0
        file_names=[]
        for filename in os.listdir(corpus_path):
            if filename.endswith(".txt") and int(filename[:filename.rfind('.')]) > self.record['files']:
                file_name_without_extension = filename[:filename.rfind('.')]
                file_names.append(int(file_name_without_extension))
                if int(file_name_without_extension) > chapter_num:
                    chapter_num = int(file_name_without_extension)

        tmp=[]
        for i in range(1,chapter_num+1):
            if i in file_names:
                tmp.append(str(i))  

        file_names=tmp

        # 对文件名进行排序  无效 1 10 100 
        # tmp=[]
        # for filename in file_names:
        #     if filename.isdigit():
        #         tmp.append(int(filename))
        # file_names=tmp
        # file_names = sorted(file_names)

        for filename in file_names:
            processed_segment_num=0

            file_path = os.path.join(corpus_path, filename+".txt")
            print(f"\n处理文件 {file_path}\n")

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 以换行符分割段落
            paragraphs = [para.strip() for para in content.split("\n") if para.strip()]

            # 合并段落，保证段落字数大于 n/2 小于 2n
            segments = []
            current_segment = ""

            # 遍历段落列表
            for para in paragraphs:
                if len(current_segment) + len(para) > 1.5 * n:
                    # 如果当前段落的长度在n/2和1.5*n之间
                    if n / 2 <= len(current_segment) <= 1.5 * n:
                        # 将当前段落添加到段落列表中
                        segments.append(current_segment.strip())
                    # 将当前段落设置为当前段落
                    current_segment = para
                # 否则
                else:
                    # 将当前段落和当前段落的长度添加到当前段落中
                    current_segment += "\n" + para

            # 如果当前段落的长度在n/2和1.5*n之间
            if n / 2 <= len(current_segment) <= 1.5 * n:
                # 将当前段落添加到段落列表中
                segments.append(current_segment.strip())

            # 创建 input, output 数据对
            for segment in segments:
                summary = self.summarize_segment(segment)
                # 将段落按句号分割为句子
                sentences = [s for s in segment.split("。") if s.strip()]
                sentences = [sentence + '。' for sentence in sentences]

                if len(sentences) > 1:
                    input_sentence = sentences[0].strip()  # 第一句作为input
                    output_text = "".join(sentences[1:]).strip()  # 其余作为output
                    p_len=len(output_text)
                    p_len=(p_len/100+1)*100  #如果555，取600

                    res={
                        "instruction": f"请按照以下描述续写小说,{p_len}字:" + summary,
                        "input": input_sentence,
                        "output": output_text
                    }

                    data.append(res)
                    add_history(self.history_path,res)

                    processed_segment_num+=1
                    update_record(self.record,filename,processed_segment_num)


            processed_segment_num=0
            update_record(self.record,filename=filename,num_done_segments=processed_segment_num)

            # 将数据和日志写入文件
            with open(output_json_path, 'r', encoding='utf-8') as json_file:
                pre_data=json.load(json_file)
            pre_data.extend(data)
            data=pre_data
            
            with open(output_json_path, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            

            # data = []  # 清空数据以进行下一个文件的处理
            file_count += 1

            elapsed_time = time.time() - start_time  # 计算已运行的时间
            logging.info(f"{file_count} files 处理完毕，数据保存到文件 {output_json_path}，已运行时间：{elapsed_time:.2f} 秒")

            if file_count >= max_files:
                break


    # 定义段落总结函数
    def summarize_segment(self,segment):
        prompt = "\n你是一个熟读各类小说的专家，请将以上小说内容确定其背景并且用一句话总结故事情节不要进行续写。严格按照以下格式回复：背景：XXXX剧情梗概：XXXX(一句话)。注意：只需提供背景和剧情梗概，不要续写正文。"
        prompt = '你现在需要分析的小说内容如下：' + segment + prompt
        if len(self.history)>0:
            his=get_history_str_by_keyword()
            prompt = f"前{CONFIG.MAX_HISTORY}章的总结："+ his + prompt
        

        messages = prompt
        role={
            "description": "\n你是一个熟读各类小说的专家，请将以上小说内容确定其背景并且用一句话总结故事情节不要进行续写。严格按照以下格式回复：背景：XXXX剧情梗概：XXXX(一句话)。注意：只需提供背景和剧情梗概，不要续写正文。",
            "options": {
                "num_keep": 5,
                "num_predict": 2000,
                "top_k": 20,
                "top_p": 0.9,
                "repeat_last_n": 33,
                "temperature": 0.8,
                "repeat_penalty": 1.2,
                "presence_penalty": 1.5,
                "num_ctx": 10240,
                "frequency_penalty": 1.0,
                "stop": ["user:", "\t", "十日终焉"]
            },
            "template":{
                "user":"",
                "assistant":""
            },
        }

        with open('template//summary_plot/user.txt', 'r', encoding='utf-8') as f:
            role['template']['user'] = f.read()
        with open('template//summary_plot//ai.txt', 'r', encoding='utf-8') as f:
            role['template']['assistant'] = f.read()
        
        response = chat_ollama_stream_post(messages,role=role)
        return response

 
    # 定义命令行参数解析
    def main(self):
        n=500
        self.history=load_history()
        self.record=load_record()
    
        # 预处理数据
        self.preprocess_data(corpus_path="input", output_dir=self.output_dir, n=n)

if __name__ == "__main__":
    Segment_Plot_Ollama_Dir().main()