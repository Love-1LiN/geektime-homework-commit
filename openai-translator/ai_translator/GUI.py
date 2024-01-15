import tkinter as tk

def main():
    window = tk.Tk()
    window.title("可视化GUI界面")

    label = tk.Label(window, text="欢迎使用可视化GUI界面！")
    label.pack()

    button = tk.Button(window, text="点击我", command=on_button_click)
    button.pack()

    window.mainloop()

def on_button_click():
    print("按钮被点击了！")

if __name__ == "__main__":
    main()
