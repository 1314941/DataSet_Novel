import os
import random
import json
import time

def cut_json(path,num):
    data=[]
    path=path.replace("\\","/")
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data=json.load(f)
                 #随机取500条数据
                import random
                if num>len(data):
                    print("数据量不足，无法随机取样。故而全部采样")
                    random_data=data
                else:
                    random_data=random.sample(data,num)

                return random_data
        else:
            print(f"文件{path}不存在")
            return data

    except Exception as e:
        print(f"加载已处理文件失败，原因：{e}")
        # exit()
        return data

   
   
def cut_jsons(paths):
    data=[]
    for path,total in paths:
        data+=cut_json(path,total)
    data=random.sample(data,len(data))

     #保存到新的json文件
    # new_path=path.replace(".json","_cut.json")
    os.makedirs("Cut",exist_ok=True)
    #时间缀 年 月 日 分 秒
    new_path=f"Cut/cutted_{time.strftime('%Y%m%d_%H_%M%S')}.json"
    # new_path="Cut/cutted.json"
    try:
        with open(new_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"保存新文件失败，原因：{e}")
        exit()

    print(f"已保存新文件：{new_path}")


if __name__ == '__main__':
    #insturction input output
    # paths=[("s_out\plot\s_corpus_processed.json",1000),
    #        ("douzhanxiyou_out\corpus_processed.json",1000),
    #        ]



    paths=[("gen_little_text_out\s_corpus_processed.json",2333)]
    cut_jsons(paths)
