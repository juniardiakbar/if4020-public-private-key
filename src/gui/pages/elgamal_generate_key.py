import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.elgamal.main import generate_pair

class ElGamalGenerateKey(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Algoritma El Gamal')

        self.render_key_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.PUBLIC_KEY_ROW = 1
        self.PRIVATE_KEY_ROW = 2
        self.BUTTON_KEY_ROW = 3
        self.public_key_dir = tk.StringVar()
        self.public_key_dir.set('')

        self.private_key_dir = tk.StringVar()
        self.private_key_dir.set('')

    def render_key_frame(self):
        public_key_frame = hg.create_frame(self, self.PUBLIC_KEY_ROW + 1)
        hg.create_label(public_key_frame, 'Public Key', 0, 0)
        hg.create_label(public_key_frame, self.public_key_dir, 0, 1, fix_text=False)
        hg.create_button(public_key_frame, 'Choose',
                         lambda: self.load_public_key(), 1, 0)

        private_key_frame = hg.create_frame(self, self.PRIVATE_KEY_ROW + 1)
        hg.create_label(private_key_frame, 'Private Key', 0, 0)
        hg.create_label(private_key_frame, self.private_key_dir, 0, 1, fix_text=False)
        hg.create_button(private_key_frame, 'Choose',
                         lambda: self.load_private_key(), 1, 0)

        button_key_frame = hg.create_frame(self, self.BUTTON_KEY_ROW + 1)
        hg.create_button(button_key_frame, 'Generate Key',
                    lambda: self.generate_key(), 1, 0)
        hg.create_button(button_key_frame, 'Back',
                    lambda: self.controller.show_frame("StartPage"), 1, 1)


    def load_public_key(self):
        dialog = fd.askopenfilename()
        self.public_key_dir.set(dialog)

    def load_private_key(self):
        dialog = fd.askopenfilename()
        self.private_key_dir.set(dialog)

    def generate_key(self):
        print('GENERATE KEY FOR EL GAMAL ALGORITHM')
        generate_pair(self.public_key_dir.get(), self.private_key_dir.get())
