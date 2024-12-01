import json
import re


"""
介绍
用于修正 fashi_out/corpus_processed.json文件

仅限以下特定情况

#[]或{}
data=[{"instruction":"你好，请问有什么可以帮到你吗？","input":"你好，请问有什么可以帮助到你吗？","output":"你好，请问有什么可以帮助到你吗？"}]
#a 追加模式
with open('fashi_out/corpus_processed_updated.json', 'a',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

会出现
"]["   和 ")("  导致json解析错误


应该先读取，更新之后以"w"模型写入的
由于代码出了bug，挂了几个小时回来才发现
不舍得直接删掉，想办法修正了过来
"""



with open('fashi_out/corpus_processed.json', 'r',encoding='utf-8') as f:
    # json_data=json.load(f)
    json_data = f.read()

json_data_updated = json_data



json_data = json_data_updated.replace("\\n", "")
# 初始化数组
instructions = []
inputs = []
outputs = []

# 匹配模式
pattern = r'"instruction": "(.*?)",\s*"input": "(.*?)",\s*"output": "(.*?)"'

# 查找所有匹配项
matches = re.findall(pattern, json_data)

# 提取匹配项并添加到数组
for match in matches:
    instructions.append(match[0])
    inputs.append(match[1])
    outputs.append(match[2])

# 打印结果
print("Instructions:", instructions)
print("Inputs:", inputs)
print("Outputs:", outputs)

data=[]
for i in range(len(instructions)):
    data.append({"instruction":instructions[i],"input":inputs[i],"output":outputs[i]})


with open('fashi_out/corpus_processed_updated.json', 'w',encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print("JSON数据已更新")



"""
#失败  成功替换 但无法识别
# json_data_updated = re.sub(r'\n]\[\s*', ',', json_data)

# json_data_updated = json_data.replace("\n][    ", ",")
# json_data_updated = json_data.replace("\n][", ",").replace("\t", "")
# json_data_updated = json_data_updated.replace("\\n", ",").replace("\r", "").replace("\n", "").replace("\\", ",")
# 打印更新后的JSON数据
# print(json_data_updated)

# 尝试解析 JSON 数据
# try:
#     data = json.loads(json_data)
# except json.JSONDecodeError as e:
#     print(f"JSON 解析错误: {e}")
#     # exit()
# print("JSON数据读取成功")

# 替换字符串
# json_data_updated = re.sub(r'\n]\[\s*', 'json', json_data)

"""