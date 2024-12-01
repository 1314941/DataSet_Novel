
import os
import json
from Gen_DataSet.config.config import CONFIG


def load_record(record_path):
    try:
        if os.path.exists(record_path):
            with open(record_path, "r", encoding="utf-8") as f:
                record=json.load(f)
                return record
    except Exception as e:
        print(f"加载已处理文件失败，原因：{e}")
        return []


def add_record(record_path,filename,segments):
    new_data={
        "filename":filename,
        "segments":segments
    }
    with open(record_path, 'r',encoding='utf-8') as file:
        record = json.load(file)
    record.append(new_data)
    with open(record_path, 'w',encoding='utf-8') as file:
        json.dump(record, file, ensure_ascii=False, indent=4)

def update_record(record_path,filename,num_done_segments):

    with open(record_path, 'r',encoding='utf-8') as file:
        record = json.load(file)

    for f in record:
        if f['filename']==filename:
            f['segments']=num_done_segments
            with open(record, 'w',encoding='utf-8') as file:
                json.dump(record, file, ensure_ascii=False, indent=4)
            return



def load_history(history_path):
    try:
        if os.path.exists(history_path):
            with open(history_path,"r",encoding="utf-8") as f:
                history.extend(json.load(f))
                return history
    except Exception as e:
        print(f"加载历史失败，原因：{e}")
        return []



def add_history(history_path,data):
    global history
    if len(history)>=CONFIG.MAX_HISTORY:
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
    try:
        if os.path.exists(result_path):
            with open(result_path, "r", encoding="utf-8") as f:
                data=json.load(f)
                return data
    except Exception as e:
        print(f"加载已处理文件失败，原因：{e}")
        return []

def add_result(result_path,data):
    with open(result_path, 'r',encoding='utf-8') as file:
        result = json.load(file)
    result.append(data)
    with open(result_path, 'w',encoding='utf-8') as file:
        json.dump(result, file, ensure_ascii=False, indent=4)