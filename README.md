# 预览
![image](https://github.com/user-attachments/assets/7bdfac11-a73c-402c-bfa0-1ca76880adb3)

# 使用指南
>1.提取事物卡之前 需要先总结  一般总结完后  第二个文本框会出现result.json文件路径 此时可开始提取事物卡  两者都需要ollama api\n
2.少量填充-no-ai 不需要api 只是随机截取片段\n
3.其他功能 都有问题 以后有空再修\n
todo:\n
  对话提取 测试效果不好 估计需要更好的**提示词**与**模型**\n
  文件夹选择  目前需要先填入路径 再点击按钮  体验很差  希望可以通过点击按钮，选择文件夹，以表格形式表示文件列表\n
  
 # 环境 
 使用的是python 3.10.14  其他的没测过
# 尝试
>模型简化   得到扩写数据集
>提取事物卡  为了提高续写效果，不吃书
>使用的模型
>llama3.1:8b 和qwen2.5:7b  

使用云端的a10，llama-factory微调，llama-cpp量化成int4模型
微调了3次，模型反而被我调傻了...
总结，电脑不好，又懒得折腾云gpu，还是用别人的模型好。
# 感谢
[Completing-Stories-Following-Instruct-with-LLMs-LoRA](https://github.com/cgxjdzz/Completing-Stories-Following-Instruct-with-LLMs-LoRA)

 
