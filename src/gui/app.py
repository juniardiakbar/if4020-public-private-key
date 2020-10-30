import tkinter as tk

from src.gui.pages.start_page import StartPage
from src.gui.pages.end_page import EndPage
from src.gui.pages.rsa_form import RSAForm
from src.gui.pages.rsa_generate_key import RSAGenerateKey
# from src.gui.pages.elgamal_form import ElgamalForm
# from src.gui.pages.diffiehellman_form import DiffieHellmanForm


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # for F in (StartPage, RSAForm, ElgamalForm, DiffieHellmanForm):
        for F in (StartPage, RSAGenerateKey, RSAForm):
            page_name = F.__name__

            frame = F(parent=self.container, controller=self)
            frame.configure(bg='white')
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def show_end_frame(self, title, file_dir, result, isTyping):
        frame = EndPage(parent=self.container, controller=self,
                        title=title, file_dir=file_dir, result=result, isTyping=isTyping)
        frame.configure(bg='white')
        frame.grid(row=0, column=0, sticky="nsew")

