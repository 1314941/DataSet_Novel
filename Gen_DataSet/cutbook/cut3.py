#将小说txt文件按章节分割，并保存到指定目录下
import os
import re


#效果比cut1.py好

def cut_book(book_path, save_path, chapters_per_file=10):
    # 打开文件，读取所有内容
    with open(book_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 正则匹配章节标题
    """
    r'第\d+章\s*(.*?)\n'：这是正则表达式模式，用原始字符串（以r开头）表示，以避免转义字符的问题。
第：匹配字符“第”。
\d+：匹配一个或多个数字。
章：匹配字符“章”。
\s*：匹配零个或多个空白字符（包括空格、制表符等）。
(.*?)：匹配任意字符（非贪婪模式），捕获组，用于提取匹配的内容。
\n：匹配换行符。
re.S：这是一个标志，表示“点号匹配所有字符”，包括换行符。默认情况下，.不匹配换行符，但加上re.S标志后，.可以匹配包括换行符在内的所有字符。
    """

   #第001章
    pattern = re.compile(r'第\d{3}章：.*')        # 定义一个正则表达式，匹配以“第”开头，后面跟着三个数字，再跟着“章：”和任意字符的字符串
   
    chapters = re.findall(pattern, content)
    chapter_texts = re.split(pattern, content)

     # 确保章节标题和章节内容一一对应
    chapter_texts = chapter_texts[1:]

    # 保存章节内容到指定目录
    for i in range(0, len(chapters), chapters_per_file):
        # 创建新的txt文件
        file_name = f"novel_part_{i//chapters_per_file + 1}.txt"
        file_path = os.path.join(save_path, file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            for j in range(i, min(i + chapters_per_file, len(chapters))):
                # 章节标题
                title = '第{}章'.format(j+1)
                # 章节内容
                content = chapters[j].strip()  #章节名
                # 写入文件
                # f.write(title)
                # f.write(content)
                # f.write('\n\n')
                print(title)
                # f.write(title)  #丞相保重 用到
                f.write(content)  #丞相保重 标题  用到  
                f.write(chapter_texts[j])
                f.write('\n\n')




if __name__ == '__main__':
    # 书籍路径
    # book_path = 'book\yinianyongheng.txt'
    book_path = 'book/fashi.txt'
    # 保存路径
    save_path = 'book/chapters'
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    # 切割小说
    cut_book(book_path, save_path, 1)
