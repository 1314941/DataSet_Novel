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


#todo
#1.总结时将适量的历史输出也输入进去 使得输出的背景不会频繁变化 （一本书一个txt文件，或者一个文件夹一本书  避免历史信息混杂，输出错乱）
#2.意外中断后，重新运行时，从上次中断的地方开始，而不是从头开始   （记录已处理的文件，从上次中断的地方开始 一个文件夹一本书）
#3.小说分章功能 将一个txt文件分成多个txt文件，每个txt文件一个章节


#1.设定好图数据库结构，构造提示词，减低模型自由度，提取信息
#2.逆向 input 前10章总结  接下来十章用到的卡片(人物，物品，地域)  output 剧情发展 标题



class Thing_Card:
    def __init__(self):
        self.history=[]

        self.output_dir = CONFIG.get_func_dir('thing_card')


        self.history_path,self.result_path,self.record_path=CONFIG.get_path(self.output_dir)


        self.data=[]
        self.record={
            "done_nums":0,
            "role_data":""
        }


    #邪门，无法保存 出了这个函数就变成""
    #bug 在一个函数里通过调用函数修改全局变量后，再调用另一个以该全局变量为参数默认值的函数，会得到未改动前的全局变量值作为默认。
    #总结 我不配...  少碰全局变量


    # 定义数据预处理函数
    def preprocess_data(self,corpus_path, n=500, batch_size=100): 

        role_data=self.record['role_data']

        # 设置日志配置
        with open(self.log_file_path, 'w', encoding='utf-8') as f:
            f.write('')
        logging.basicConfig(
            filename=self.log_file_path,  # 日志文件名
            level=logging.INFO,       # 日志级别
            format='%(asctime)s - %(message)s',  # 日志格式
            filemode='a'              # 追加模式
        )


        record=self.record['done_nums']
        processed_segment_num=record

        start_time = time.time()
        # 遍历语料库路径下的所有txt文件
        input_data=load_result(corpus_path)
            
        processing_segment_num=0
        for f in input_data:

            processing_segment_num+=1
    
            if processing_segment_num<=processed_segment_num:
                continue

            #效果太差了  总提取出鸡肉这些无关紧要的东西  或者直接续写了(提示词没提到续写，初步怀疑是因为每简化十章才提取一次，上下文还保留着，导致模型混乱)  
            #应该先总结完再提取角色卡片  迭代几次后效果可能好点
            total=10
            count=0
            content=""
            for f in input_data:
                count+=1

                if processing_segment_num<=count and processing_segment_num+total>count:
                    content+=f['instruction'].replace("请按照以下描述续写小说,","")

            print(f"\n处理 {processing_segment_num}_{processing_segment_num+total}\n")
            role_data=self.get_character_card(content,role_data)
            processed_segment_num+=total


            res={
                "input": content,
                "output": role_data
            }

            self.data.append(res)

            add_history(self.history_path,res)

            update_record(self.record_path,processing_segment_num)

            # 将数据和日志写入文件
            with open(self.result_path, 'w', encoding='utf-8') as json_file:
                json.dump(self.data, json_file, ensure_ascii=False, indent=4)


        
            elapsed_time = time.time() - start_time  # 计算已运行的时间


        logging.info(f"处理完毕，数据保存到文件 {self.result_path}，已运行时间：{elapsed_time:.2f} 秒")        
        #-1代表完成
        update_record(-1)


    def get_character_card(self,input_data,role_data):
        total=10
        count=0
        content=input_data


        role_data=""        
        if role_data=="":
            content="最新章节发展:"+content
        else:
            content="事物原形象:"+role_data+"最新章节发展:"+content
        role_data = self.chat_for_role(content)

        return role_data


    def chat_for_role(sentence):
        prompt = sentence

        #人物卡最多4张,物品卡最多2张。
        limit_num=666

        messages = prompt+f"{limit_num}字以内"
        role={
            "description": f"""\n你是一个熟读各类小说的设定专家,现在需要你提取出输入的小说里的事物的形象和设定，并以规范的
            卡片形式描述出来。将输出控制在{limit_num}字以内。只能输出主要的人物和物品,不能输出配角和道具。
            事物的指定范围包括人物，罕见的宝物，武器,和新出现的地域等。注意，情感，性格，一般的生活物品，年龄和事件等因素不在此范围。
            如果出现了变化，请及时更新并着重提取。出现率太低的可以不管。
            输出规范
            人物:
            -形象
            -特点
            -变化(有变化时出现)
            物品:
            -特点
            -作用
            """,
            "options": {
                "num_keep": 5,
                "num_predict": limit_num,
                "top_k": 15,
                "top_p": 0.9,
                "repeat_last_n": 33,
                "temperature": 0.2,
                "repeat_penalty": 1.5,
                "presence_penalty": 1.9,
                "num_ctx": 10240,
                "frequency_penalty": 1.0,
                "stop": ["user:", "\t", "十日终焉"]
            },
            "template":{
                "user":"",
                "assistant":""
            },
        }

        with open('template/thing_card/user.txt', 'r', encoding='utf-8') as f:
            role['template']['user'] = f.read()
        with open('template/thing_card/ai.txt', 'r', encoding='utf-8') as f:
            role['template']['assistant'] = f.read()
        
        response = chat_ollama_stream_post(messages,role=role)
        return response



    #提取角色卡片
    def work(self,input_file="result.json",n=500):
        #300太小  
        n=666
        self.history=load_history(history_path=self.history_path)
        # print(record_path)
        self.record=load_record(record_path=self.record_path)
        # print(record)
        self.data=load_result(result_path=self.result_path)
    
        # 预处理数据
        corpus_path = input_file.replace("\\", "/")
        # print(f"corpus_path: {corpus_path}")

        self.preprocess_data(corpus_path=corpus_path, n=n)


# if __name__ == '__main__':
    # Thing_Card().work();