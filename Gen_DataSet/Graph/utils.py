import random
import threading
import time
import os
import gradio as gr
import shutil
from Gen_DataSet.AI.summary_plot import Summary
from Gen_DataSet.NOAI.gen_little_text_thread import Gen_Little_Text_Thread
from Gen_DataSet.AI.thing_card import Thing_Card


def middle_chat(messages,history):

    carrier = threading.Event()
    carrier.history = history
    # if len(carrier.history) > 20:
    #     carrier.history = carrier.history[-16:]
    try:
        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"\n{messages}"

        output_text = ""

        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"\n{output_text}"

        return carrier
    
    except Exception as e:
        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"Error: {e}"
        raise carrier


def list_txt_files(folder_path):

    if os.path.isdir(folder_path):
        txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        return "\n".join(txt_files)
    else:
        return "请选择一个有效的文件夹路径。"

def on_folder_select(folder_path):
    folder_path = gr.File()
    return folder_path



def gen_ouline_button_clicked(question, history):
    carrier = middle_chat(question,history)

    yield [
        carrier.history,
        gr.Button(visible=True)
    ]


def select_file(file_obj):
    FilePath=file_obj.name

    # 获取上传Gradio的文件名称
    FileName=os.path.basename(file_obj.name)
    print(FilePath)
    #获取父文件夹
    ParentFolder=os.path.dirname(FilePath)
    print(ParentFolder)

    # 返回新文件的的地址（注意这里）
    return ParentFolder

def create_choose_talk(start_symbol,end_symbol):
        start_options = ["“",":"]
        end_options = ["”","。"]

        return gr.Radio(
            choices=start_options,
            label="选择对话开始符号",
            value=start_symbol,
        ),gr.Radio(
            choices=end_options,
            label="选择对话结束符号",
            value=end_symbol,
        )

def create_choose_heart(start_symbol,end_symbol):
        start_options = ["‘","["]
        end_options = ["’","]"]

        return gr.Radio(
            choices=start_options,
            label="选择对话开始符号",
            value=start_symbol,
        ),gr.Radio(
            choices=end_options,
            label="选择对话结束符号",
            value=end_symbol,
        )


def on_summary_button(path):
    #返回 结果json文件路径  事物卡提取需要
    path=Gen_Little_Text_Thread().work(path)
    return path

def on_thing_card_button(path):
    Thing_Card().work(path)


def on_little_text_button(path):
    Summary().work(path)


