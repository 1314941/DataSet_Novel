
import os
import json
from Gen_DataSet.config.config import CONFIG

def load_json(json_path):
    try:
        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                record=json.load(f)
                return record
        else:
            print(f"未找到已处理文件\n")
            choice=input("是否从头开始？(y/n)")
            if choice=='y':
                return []
            else:
                exit()
    except Exception as e:
        print(f"加载已处理文件失败，原因：{e}")
        return []
    



def load_record(record_path):
    return load_json(record_path)

def add_record(record_path,filename,segments):
    new_data={
        "filename":filename,
        "segments":segments
    }
    if os.path.exists(record_path):
        with open(record_path, 'r',encoding='utf-8') as file:
            record = json.load(file)
    else:
        record=[]
    record.append(new_data)
    with open(record_path, 'w',encoding='utf-8') as file:
        json.dump(record, file, ensure_ascii=False, indent=4)


def update_record(record_path,filename,segments):
    with open(record_path, 'r',encoding='utf-8') as file:
        record = json.load(file)

    for f in record:
        if f['filename']==filename:
            f['segments']=segments
            with open(record_path, 'w',encoding='utf-8') as file:
                json.dump(record, file, ensure_ascii=False, indent=4)
            return



def load_history(history_path):
   return load_json(history_path)



def add_history(history_path,data):
    if os.path.exists(history_path):
        with open(history_path, 'r',encoding='utf-8') as file:
            history = json.load(file)
    else:
        history=[]
    while len(history)>=CONFIG.MAX_HISTORY:
        history.pop(0)
    history.append(data)
    with open(history_path,"w",encoding="utf-8") as f:
        json.dump(history,f,ensure_ascii=False,indent=4)


def get_history_str_by_keyword(keyword='instuction'):
    history=""
    count=1
    for data in history:
        history+=("\n###"+str(count)+"\n"+data[keyword]+'###\n')
    return history




def load_result(result_path):
    return load_json(result_path)

def add_result(result_path,data):
    with open(result_path, 'r',encoding='utf-8') as file:
        result = json.load(file)
    result.append(data)
    with open(result_path, 'w',encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

def save_result(result_path,data):
    with open(result_path, 'w',encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)