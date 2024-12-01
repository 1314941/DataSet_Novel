import argparse
import ollama
import os
import requests
import json
import re
import time
import logging
from Gen_DataSet.config.config import CONFIG
from Gen_DataSet.util.util import add_history,add_record,add_result,update_record,load_history,load_record,load_result,get_history_str_by_keyword
from Gen_DataSet.chat.chat import chat_ollama_stream_post
from Gen_DataSet.config.template_cf import read_template

class FillText:
  def __init__(self):
        self.history=[]

        self.output_dir = CONFIG.get_func_dir('fill_text')


        self.history_path,self.result_path,self.record_path=CONFIG.get_path(self.output_dir)


        self.data=[]
        self.record={
            "done_nums":0,
            "role_data":""
        }

#bug 在一个函数里通过调用函数修改全局变量后，再调用另一个以该全局变量为参数默认值的函数，会得到未改动前的全局变量值作为默认。
#总结 我不配...  少碰全局变量


# 定义数据预处理函数
def preprocess_data(self,corpus_path, output_dir="s_out", n=500, batch_size=100): 

    role_data=record['role_data']

    # 设置日志配置
    with open(self.log_file_path, 'w', encoding='utf-8') as f:
        f.write('')
    logging.basicConfig(
        filename=self.log_file_path,  # 日志文件名
        level=logging.INFO,       # 日志级别
        format='%(asctime)s - %(message)s',  # 日志格式
        filemode='a'              # 追加模式
    )


    # record=[]
    # for f in result:
    #     record.append(f['segments'])
    record=record['done_nums']
    processed_segment_num=record

    start_time = time.time()
    # 遍历语料库路径下的所有txt文件
    input_data=load_result(corpus_path)
           
    processing_segment_num=0
    for f in input_data:

        processing_segment_num+=1
  
        #效果太差了  总提取出鸡肉这些无关紧要的东西  或者直接续写了(提示词没提到续写，初步怀疑是因为每简化十章才提取一次，上下文还保留着，导致模型混乱)  
        # if processing_segment_num%10==1:
            # role_data=get_character_card(processing_segment_num)

        if processing_segment_num<=processed_segment_num:
            continue

        print(f"\n处理 {processing_segment_num}\n")
        content=f['input']+f['output']
        
   
        simple_sentence = simplify_sentence(content)

        res={
            "instruction": f"""\n你是一个熟读各类小说的专家,请对输入的小说总结进行分析,并为小说草稿填充合理的细节。
            一定记住，不能向小说草稿里添加任何对于本次改动的想法或评价,不能添加与小说内容无关的东西。！！！
            注意：要分析并根据人物的性格填充合理的内容。
            请对小说草稿进行完善,注意，如果没找到合理的地方填充,不要强行填充,只要润色文笔即可！
            """,
            "input": simple_sentence,
            "output": content
        }

        self.data.append(res)

        self.add_history(self.history_path,res)


        update_record(processing_segment_num)

        # 将数据和日志写入文件
        with open(self.result_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.data, json_file, ensure_ascii=False, indent=4)


     
        elapsed_time = time.time() - start_time  # 计算已运行的时间


    logging.info(f"处理完毕，数据保存到文件 {self.result_path}，已运行时间：{elapsed_time:.2f} 秒")        
    #-1代表完成
    update_record(-1)



    # 简化句子
    def simplify_sentence(self,sentence):
        # prompt = "\n你是一个熟读各类小说的专家，请对输入的小说总结进行分析,并为小说草稿填充富有人物特色的对话。注意：要分析并根据人物的性格填充合理的对话。"
        prompt = """\n你是一个熟读各类小说的专家,现在需要你对输入的小说草稿进行简化或删减,以在保证小说内容完整，情节合理的前提下缩减小说篇幅。
                    一定记住，不能向小说草稿里添加任何对于本次改动的想法或评价,不能添加与小说内容无关的东西。！！！
                    注意，如果没找到合理的地方处理,不要强行删改"""

        prompt = '你现在需要简化或删减的小说草稿如下：' + sentence + prompt
        p_len=len(sentence)
        p_len=(int(p_len/100)+1)*100  #如果555，取600

        messages = prompt
        role={
            "description": """\n你是一个熟读各类小说的专家,现在需要你对输入的小说草稿进行简化或删减,以在保证小说内容完整，情节合理的前提下缩减小说篇幅。
                    一定记住，不能向小说草稿里添加任何对于本次改动的想法或评价,不能添加与小说内容无关的东西。！！！
                    注意，如果没找到合理的地方处理,不要强行删改""",
            "options": {
                "num_keep": 5,
                "num_predict": p_len,
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

        with open('template/talk/user.txt', 'r', encoding='utf-8') as f:
            role['template']['user'] = f.read()
        with open('template/talk/ai.txt', 'r', encoding='utf-8') as f:
            role['template']['assistant'] = f.read()
        
        response = chat_ollama_stream_post(messages,role=role)
        return response


    # 定义命令行参数解析
    def work(self,input_path):
        #300太小  
        n=666
        self.history=load_history(self.history_path)
        self.record=load_record(self.record_path)
        self.result=load_result(self.result_path)
    
        # 预处理数据
        self.preprocess_data(corpus_path=input_path, n=n)


# if __name__ == '__main__':
    # FillText().work(input_path='s_out')