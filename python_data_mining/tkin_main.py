import tkinter as tk
from tkinter import ttk
import nearMe as miner
import time

class SampleApp:
    def __init__(self):
        self.main = tk.Tk()
        self.main.title("Data Miner")
        self.searchbox = tk.Label(self.main, text="Search: ")
        self.searchbox.pack()

        self.w = tk.Entry(self.main, bd = 5)
        self.w.pack()

        self.button = tk.Button(self.main, text='start', width=25, command=self.startTheMining)
        self.button.pack()

        self.progress = tk.ttk.Progressbar(self.main, orient="horizontal", length=200, mode="determinate")
        self.progress.pack()

        self.main.mainloop()

    def startTheMining(self):
        if not self.w.get():
            self.msg = tk.Message(m, text="The text is empty.")
            self.msg.pack()

        else:
            miner.main_start(search = self.w.get())

app = SampleApp()


"""
    m = tk.Tk()
    m.title('Data Miner')
    label1 = tk.Label(m, text="Search: ")
    label1.pack()
    w = tk.Entry(m, bd = 5)
    w.pack()

    #miner.main_start
    button = tk.Button(m, text='start', width=25, command=startTheMining)
    button.pack()

    progress = tk.ttk.Progressbar(m, orient="horizontal", length=200, mode="determinate")
    progress.pack()

    m.mainloop()
"""
