import os
import json


def get_time_stamp():
    import time
    return time.strftime("%Y%m%d_%H%M%S", time.localtime())





class Config:
    def __init__(self):
        self.record_path = "record.json"
        
        # 单个文件
        self.SINGLE_PREFIX = "single"
        self.DIR_PREFIX = "dir"  

        self.HISTORY_FILE="history.json"
        self.RESULT_FILE = "result.json"
        self.RECORD_FILE = "record.json"

        self.MAX_HISTORY = 10

        self.MODEL_NAME= "novel"



    def set_data_root(self, data_root):
        # 数据根目录
        self.DATA_ROOT = data_root

        self.INPUT_DIR = os.path.join(self.DATA_ROOT, "input")
        self.OUTPUT_DIR = os.path.join(self.DATA_ROOT, "output")
        self.TEMPLATE_DIR = os.path.join(self.DATA_ROOT, "template")

    def save_json(self, func_name, time_stamp):
        try:
            if os.path.exists(self.record_path):
                with open(self.record_path, "r", encoding="utf-8") as f:
                    record=json.load(f)
            else:
                record={}

            record[f'{func_name}'] = time_stamp

            with open(self.record_path, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=4)
        except Exception as e:
            print(f"保存已处理文件失败，原因：{e}")
            raise e


    def read_json(self, func_name):
        try:
            if os.path.exists(self.record_path):
                with open(self.record_path, "r", encoding="utf-8") as f:
                    record=json.load(f)
                    return record[f'{func_name}']
            else:
                    time_stamp=get_time_stamp()
                    self.save_json(func_name, time_stamp)
                    return time_stamp
        except Exception as e:
            print(f"加载已处理文件失败，原因：{e}")
            # return get_time_stamp()
            raise e



    def get_func_dir(self,func_name):
        last_time=self.read_json(func_name)
        func_path=os.path.join(self.OUTPUT_DIR, f"{func_name}", f"{last_time}")
        return func_path



    def get_path_with_prefix(self,dir, single=True):
        if single:
            prefix = self.SINGLE_PREFIX
        else:
            prefix = self.DIR_PREFIX

        history=os.path.join(dir, prefix + "_" + self.HISTORY_FILE)
        result=os.path.join(dir, prefix + "_" + self.RESULT_FILE)
        record=os.path.join(dir, prefix + "_" + self.RECORD_FILE)
        return history, result, record



 
CONFIG = Config()