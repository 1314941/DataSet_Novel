import random
import threading
import time

import gradio as gr




#斜眼抑制
# 电机械分离现象
# 腰膝酸软
# 右室肥厚
# 疥疮恐惧

# 对数据进行个性化词云展示



def middle_chat(messages,history):

    carrier = threading.Event()
    carrier.history = history
    # if len(carrier.history) > 20:
    #     carrier.history = carrier.history[-16:]
    try:
        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"\n{messages}"

        output_text = handler.chat_main(messages)

        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"\n{output_text}"

        return carrier
    
    except Exception as e:
        carrier.history.append([None, ""])

        carrier.history[-1][1] = f"Error: {e}"
        raise carrier



def gen_ouline_button_clicked(question, history):

    carrier = middle_chat(question,history)

    yield [
        carrier.history,
        gr.Button(visible=True)
    ]




css = """
#row1 {
    min-width: 200px;
    max-height: 700px;
    overflow: auto;
}
#row2 {
    min-width: 300px;
    max-height: 700px;
    overflow: auto;
}
"""


"""
gr.State是Gradio库中的一个类，用于创建和管理状态变量。状态变量在Gradio应用的生命周期内保持其值不变，
可以在多个组件之间共享。
AIGN(chatLLM)是一个函数调用，它接受chatLLM作为参数，并返回一个值。这个值被赋给状态变量aign。
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown("## ai医疗知识图谱问答系统 Demo")
    gr.Markdown("### 快乐每一天")
    with gr.Row():
        with gr.Column(scale=0, elem_id="row1"):
            with gr.Tab("开始"):

                user_text = gr.Textbox(
                    "",
                    label="输入",
                    lines=4,
                    interactive=True,
                )

                ask_button = gr.Button("发送")
           
         
        with gr.Column(scale=3, elem_id="row2"):
            chatBox = gr.Chatbot(height=f"80vh", label="输出")


    gr.Markdown("github:QABasedOnMedicaKnowledgeGraph")

    ask_button.click(
        gen_ouline_button_clicked,
        [user_text, chatBox],
        [chatBox, ask_button],
    )
 

demo.queue()
demo.launch()
