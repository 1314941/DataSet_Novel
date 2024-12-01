import random
import threading
import time
import os
import gradio as gr
from Gen_DataSet.Graph.utils import *




css = """
#row1 {
    min-width: 200px;
    max-height: 700px;
    overflow: auto;
}
"""


"""
gr.State是Gradio库中的一个类，用于创建和管理状态变量。状态变量在Gradio应用的生命周期内保持其值不变，
可以在多个组件之间共享。
AIGN(chatLLM)是一个函数调用，它接受chatLLM作为参数，并返回一个值。这个值被赋给状态变量aign。
"""


info=\
"""
1.提取事物卡之前 需要先总结  一般总结完后  第二个文本框会出现result.json文件路径 此时可开始提取事物卡  两者都需要ollama api\n
2.少量填充-no-ai 不需要api 只是随机截取片段\n
3.其他功能 都有问题 以后有空再修\n
todo:\n
  对话提取 测试效果不好 估计需要更好的**提示词**与**模型**\n
  文件夹选择  目前需要先填入路径 再点击按钮  体验很差  希望可以通过点击按钮，选择文件夹，以表格形式表示文件列表\n
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("## 小说数据集生成器")
    gr.Markdown("### 20241201")
    with gr.Accordion("使用指南"):
        # 在折叠面板中添加Markdown格式的信息
        gr.Markdown(info)
    with gr.Row():
        # with gr.Column(scale=0, elem_id="row1"):
            with gr.Tab("开始"):

                gr.Markdown("### 生成选项")
                folder1_path = gr.Textbox(
                    "",
                    label="文件夹路径",
                    lines=1,
                    interactive=True,
                )
                summary_button = gr.Button("总结")

                
                folder2_path = gr.Textbox(
                    "",
                    label="文件夹路径",
                    lines=1,
                    interactive=True,
                )
                thing_card_button = gr.Button("事物卡")
                
                folder3_path = gr.Textbox(
                    "",
                    label="文件夹路径",
                    lines=1,
                    interactive=True,
                )
                little_text_button = gr.Button("少量填充-no-ai")


                summary_button.click(on_summary_button, inputs=folder1_path,outputs=folder2_path)
                little_text_button.click(on_little_text_button, inputs=folder3_path)
                thing_card_button.click(on_thing_card_button, inputs=folder2_path)

            with gr.Tab("对话和心理活动提取"):
                gr.Markdown("### 对话提取")
                #下拉框
                create_choose_talk("“","”")

                start1_button = gr.Button("开始")

                gr.Markdown("### 心理活动提取")
                #下拉框
                create_choose_heart("‘","’")

                start2_button = gr.Button("开始")



           
            with gr.Tab("文件列表"):
                folder_path = gr.Textbox(
                    "",
                    label="文件夹路径",
                    lines=1,
                    interactive=True,
                )
                folder_button = gr.Button("选择文件夹")
                folder_button.click(on_folder_select, inputs=folder_path, outputs=folder_path)
                file_list = gr.Textbox(
                    "",
                    label="txt文件列表",
                    lines=10,
                    interactive=False,
                )
                folder_button.click(lambda folder_path: list_txt_files(folder_path), inputs=folder_path, outputs=file_list)





        # with gr.Column(scale=3, elem_id="row3"):
        #     inputs = gr.components.File(label="上传文件")
        #     outputs = gr.Textbox(
        #             "",
        #             label="文件夹路径",
        #             lines=1,
        #             interactive=True,
        #         )

        #     folder_button = gr.Button("选择文件夹")
        #     folder_button.click(select_file, inputs=inputs, outputs=outputs)
        #     file_list = gr.Textbox(
        #         "",
        #         label="txt文件列表",
        #         lines=10,
        #         interactive=False,
        #     )
        #     folder_button.click(lambda folder_path: list_txt_files(outputs), inputs=folder_path, outputs=file_list)


