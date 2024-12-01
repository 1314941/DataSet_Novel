import requests
import json
from Gen_DataSet.config.config import CONFIG



def chat_ollama_stream_post(message:str,role:dict):
    
        tokens = message
        #写入文件
        base_url ="http://localhost:11434/api/generate"
        if role['template']['user']=="none" or role['template']['assistant']=="none":
            pass
        else:
            tokens ="\n示例开始:\nuser:\n```\n"+role['template']['user'] + "\n```\nassistant:\n```\n" + role['template']['assistant']+"\n```\n示例结束。\n"+tokens
        
        # print(f"ollama chat: \n{tokens}\n")

        data = {
            "model": CONFIG.MODEL_NAME,
            "system": role['description'], 
            "options": role['options'], 
            "prompt": tokens,
            "stream": True
        }
        response = requests.post(base_url, json=data, stream=True)
        content=""
        print("ollama result:\n")
        for line in response.iter_lines():
            line = json.loads(line.decode('utf-8'))
            if isinstance(line, dict):  # 确保 line 是字典类型  generate 接口 返回response 字段
                text = line['response']
            else:
                data = json.loads(line)  # 使用 JSON 加载
                text = data['response']
            print(text, end='')
            content += text
        print("\n")
    
        return content
