import tkinter as tk
from tkinter import filedialog

def upload_file():
    file_path = filedialog.askopenfilename()
    print("选择的文件路径为：", file_path)

app = tk.Tk()
app.title("文件上传")

upload_button = tk.Button(app, text="上传文件", command=upload_file)
upload_button.pack()

app.mainloop()