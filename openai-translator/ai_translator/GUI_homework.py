import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

from openai import OpenAI
from translator.pdf_parser import PDFParser

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

# 第一个界面类
class FirstWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Uploader")

        # 上传按钮
        self.upload_button = tk.Button(self.master, text="Upload PDF", command=self.upload_pdf)
        self.upload_button.pack(pady=20)
        self.pdf_parser = PDFParser()

    def upload_pdf(self):
        # 弹出文件选择对话框
        file_path = filedialog.askopenfilename(
            title="Select a PDF File",
            filetypes=[("PDF files", "*.pdf")]  # 限制只能选择PDF文件
        )

        # 如果用户选择了一个文件
        if file_path:
            # 获取文件名
            file_name = os.path.basename(file_path)

            # 指定保存路径为当前工作目录
            save_path = os.path.join(os.getcwd(), file_name)

            # 如果文件已经存在，可以选择覆盖或跳过
            if os.path.exists(save_path):
                overwrite = messagebox.askyesno("File Exists",
                                                f"The file '{file_name}' already exists. Do you want to overwrite it?")
                if not overwrite:
                    return  # 如果用户选择不覆盖，则退出函数

            # 复制文件到当前目录
            shutil.copy2(file_path, save_path)

            # 弹出消息框确认文件已上传
            messagebox.showinfo("Success", f"The file '{file_name}' has been uploaded successfully.")

            text = self.pdf_parser.parse_pdf(save_path)
            original = text.pages[0].contents[0].original
            instruction = f"将下列文本翻译成中文:\n{original}"
            translation = get_completion(instruction)

            # 隐藏当前窗口并显示第二个窗口
            self.master.withdraw()
            self.second_window = SecondWindow(self.master, original, translation)
            self.master.wait_window(self.second_window.top)

            # 如果需要，可以在这里销毁第一个窗口
            # self.master.destroy()


# 第二个界面类
class SecondWindow:
    def __init__(self, master, original, translation):
        self.top = tk.Toplevel(master)
        self.top.title("Second Window")

        # 第一个文本框
        self.text_frame1 = tk.Frame(self.top)
        self.text_frame1.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_box1 = tk.Text(self.text_frame1, wrap=tk.NONE)
        self.text_scroll1 = tk.Scrollbar(self.text_frame1, command=self.text_box1.yview)
        self.text_box1['yscrollcommand'] = self.text_scroll1.set

        self.text_box1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_scroll1.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box1.insert(tk.END, original)  # 插入长文本

        # 分割线
        self.separator = tk.Frame(self.top, height=2, bd=1, relief=tk.SUNKEN)
        self.separator.pack(fill=tk.X, padx=5, pady=5)

        # 第二个文本框
        self.text_frame2 = tk.Frame(self.top)
        self.text_frame2.pack(fill=tk.BOTH, expand=True, pady=10)

        self.text_box2 = tk.Text(self.text_frame2, wrap=tk.NONE)
        self.text_scroll2 = tk.Scrollbar(self.text_frame2, command=self.text_box2.yview)
        self.text_box2['yscrollcommand'] = self.text_scroll2.set

        self.text_box2.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_scroll2.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box2.insert(tk.END, translation)  # 插入长文本

# 创建主窗口并运行程序
root = tk.Tk()
app = FirstWindow(root)
root.mainloop()