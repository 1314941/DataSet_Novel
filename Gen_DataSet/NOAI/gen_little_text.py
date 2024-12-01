import argparse
import ollama
import os
import requests
import json
import random
import re
import time
import logging
from Gen_DataSet.config.config import CONFIG
from Gen_DataSet.util.util import add_history,add_record,add_result,update_record,load_history,load_record,load_result,get_history_str_by_keyword


#没测试，仅供回忆，多线程速度更快

#todo
#1.总结时将适量的历史输出也输入进去 使得输出的背景不会频繁变化 （一本书一个txt文件，或者一个文件夹一本书  避免历史信息混杂，输出错乱）
#2.意外中断后，重新运行时，从上次中断的地方开始，而不是从头开始   （记录已处理的文件，从上次中断的地方开始 一个文件夹一本书）
#3.小说分章功能 将一个txt文件分成多个txt文件，每个txt文件一个章节

class Gen_Little_Text:
    def __init__(self):
        self.output_dir = CONFIG.get_func_dir("gen_little_text_output")
        self.history_path,self.result_path,self.record_path=CONFIG.get_path_with_prefix(self.output_dir)

        self.record=[]
        self.history=[]


        self.data=[]




    # 定义数据预处理函数
    def preprocess_data(self,corpus_path="input", n=500, batch_size=100): 

        # 确保输出目录存在
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        log_file_path = os.path.join(self.output_dir, '.log')

    
        file_count = 0
        max_files = 205027

        # 设置日志配置
        logging.basicConfig(
            filename=log_file_path,  # 日志文件名
            level=logging.INFO,       # 日志级别
            format='%(asctime)s - %(message)s',  # 日志格式
            filemode='a'              # 追加模式
        )

    

        processed_file_names=[f['filename'] for f in self.record]
        start_time = time.time()
        # 遍历语料库路径下的所有txt文件
        file_names=[]
        for filename in os.listdir(corpus_path):
            has_add=False
            if filename.endswith(".txt"):
                if filename not in processed_file_names:
                    file_names.append([filename,0,has_add])
                for f in self.record:
                    if f['filename']==filename and f['segments']!=-1:
                        has_add=True
                        file_names.append([filename,f['segments'],has_add])
            

        for f in file_names:
            processing_segment_num=0
            filename=f[0]
            processed_segment_num=f[1]

            file_path = os.path.join(corpus_path, filename)
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
                processing_segment_num+=1

                if processing_segment_num<=processed_segment_num:
                    continue
                # summary = summarize_segment(segment)


                has_add=f[2]
                if not has_add:
                    add_record(self.record_path,filename,0)
                    f[2]=True
                

                # 将段落按句号分割为句子
                sentences = [s for s in segment.split("。") if s.strip()]
                sentences = [sentence + '。' for sentence in sentences]

                if len(sentences) > 1:
                    # output_text = sentences[-1].strip()  # 最后一句作为input
                    # input_sentence = "".join(sentences[:-2]).strip()  # 其余作为output

                    random_index  = random.randint(0, len(sentences) - 1)  # 随机选择一个句子作为output
                    output_text = sentences[random_index].strip()  # 随机选择的句子作为output
                    random_other=random.randint(0, len(sentences[random_index-1])-1)
                    output_text=sentences[random_index-1][random_other+1:]+output_text
                    
                    # 创建一个新的字符串，将random_other个字符替换为"_"
                    new_sentence = sentences[random_index-1][:random_other] + ">_< "

                    sentences[random_index-1]=new_sentence
                    # sentences[random_index]="_"*len(sentences[random_index])
                    sentences[random_index]=" >_<"
                    input_sentence = "".join(sentences).strip()  # 所有句子作为input
                    # p_len=len(output_text)
                    # p_len=(int(p_len/100)+1)*100  #如果555，取600

                    res={
                        # "instruction": f"请按照以下描述续写小说,{p_len}字:" + summary,
                        "input": input_sentence,
                        "output": output_text
                    }

                    self.data.append(res)

                    add_history(self.history_path,res)


                    update_record(self.record_path,filename,processing_segment_num)

                    # 将数据和日志写入文件
                    with open(self.result_path, 'w', encoding='utf-8') as json_file:
                        json.dump(self.data, json_file, ensure_ascii=False, indent=4)

            
            #-1代表完成
            update_record(self.record_path,filename,-1)
            file_count += 1

            elapsed_time = time.time() - start_time  # 计算已运行的时间


            logging.info(f"{file_count} files 处理完毕，数据保存到文件 {self.result_path}，已运行时间：{elapsed_time:.2f} 秒")        
            if file_count >= max_files:
                break


    # 定义命令行参数解析
    def main(self,input_path):
        #300太小  
        n=666
        load_history(self.history_path)
        load_record(self.record_path)
        load_result(self.result_path)
        # 预处理数据
        self.preprocess_data(corpus_path=input_path, output_dir=self.output_dir, n=n)

if __name__ == "__main__":
    Gen_Little_Text().main()
