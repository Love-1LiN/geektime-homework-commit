import tkinter as tk

from translator.pdf_parser import PDFParser
from openai import OpenAI

client = OpenAI(
    api_key="sk-N9ByicG2IQn84YmScue2wD3xKutgr3dEnAhPI7qDXdaCFTMb",
    base_url="https://api.fe8.cn/v1"
)

def get_completion(prompt, model="gpt-3.5-turbo-16k"):      # 默认使用 gpt-3.5-turbo 模型
    messages = [{"role": "user", "content": prompt}]    # 将 prompt 作为用户输入
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,                                  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

pdf_file_path = "../tests/test.pdf"
pdf_parser = PDFParser()
res = pdf_parser.parse_pdf(pdf_file_path)

text = res.pages[0].contents[0].original

target_language = '中文'

instruction = f"将下列文本翻译成{target_language}:\n{text}"

res = get_completion(instruction)

# 创建主窗口
root = tk.Tk()
root.title("Hello World App with Separator")

# 创建一个标签（文本框），并设置其文本为"Hello World"
label1 = tk.Label(root, text=text)
label1.pack(pady=10)  # pady 参数增加垂直方向上的填充，使标签与分割线之间有间隔

# 创建一个分割线（使用Frame实现）
separator = tk.Frame(root, height=2, bd=1, relief=tk.SUNKEN)
separator.pack(fill=tk.X, padx=10)  # fill=X 使分割线水平填充，padx 增加水平方向上的填充

# 创建第二个标签（文本框），并设置其文本为"Hi man"
label2 = tk.Label(root, text=res)
label2.pack(pady=10)  # 同样增加垂直方向上的填充

# 开始主事件循环
root.mainloop()

