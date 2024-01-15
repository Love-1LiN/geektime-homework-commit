import tkinter as tk
from tkinter import filedialog
import os
import shutil

# 创建主窗口
root = tk.Tk()
root.title("PDF Uploader")


def upload_pdf():
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
            overwrite = tk.messagebox.askyesno("File Exists",
                                               f"The file '{file_name}' already exists. Do you want to overwrite it?")
            if not overwrite:
                return  # 如果用户选择不覆盖，则退出函数

        # 复制文件到当前目录
        shutil.copy2(file_path, save_path)

        # 弹出消息框确认文件已上传
        tk.messagebox.showinfo("Success", f"The file '{file_name}' has been uploaded successfully.")

    # 创建上传按钮


upload_button = tk.Button(root, text="Upload PDF", command=upload_pdf)
upload_button.pack(pady=20)

# 开始主事件循环
root.mainloop()