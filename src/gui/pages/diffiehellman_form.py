import time
import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.diffiehellman.main import generate_symmetric_key


class DiffieHellmanForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Pembangkitan Kunci Diffiel-Hellman')

        self.render_n_frame()
        self.render_g_frame()
        self.render_x_frame()
        self.render_y_frame()
        self.render_execute_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.N_ROW = 1
        self.G_ROW = 2
        self.X_ROW = 3
        self.Y_ROW = 4
        self.EXECUTE_ROW = 5

        self.n_option = tk.IntVar()
        self.n_option.set(0)

        self.g_option = tk.IntVar()
        self.g_option.set(0)

        self.x_option = tk.IntVar()
        self.x_option.set(0)

        self.y_option = tk.IntVar()
        self.y_option.set(0)

    def render_n_frame(self):
        self.n_frame = hg.create_frame(self, self.N_ROW + 1)
        hg.create_label(self.n_frame, 'Bilangan Prima N', 0, 0)
        self.n_entry = hg.create_entry(self.n_frame, "", 1, 0)

    def render_g_frame(self):
        self.g_frame = hg.create_frame(self, self.G_ROW + 1)
        hg.create_label(self.g_frame, 'Bilangan G (G < N)', 0, 0)
        self.g_entry = hg.create_entry(self.g_frame, "", 1, 0)

    def render_x_frame(self):
        self.x_frame = hg.create_frame(self, self.X_ROW + 1)
        hg.create_label(self.x_frame, 'Bilangan Alice X', 0, 0)
        self.x_entry = hg.create_entry(self.x_frame, "", 1, 0)

    def render_y_frame(self):
        self.y_frame = hg.create_frame(self, self.Y_ROW + 1)
        hg.create_label(self.y_frame, 'Bilangan Bob Y', 0, 0)
        self.y_entry = hg.create_entry(self.y_frame, "", 1, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def execute(self):
        print('Diffie-Hellman Session Key Generation Started!')
        print('> Prime Number N:', self.n_entry.get())
        print('> Integer G:', self.g_entry.get())
        print('> Alice\'s Number X:', self.x_entry.get())
        print('> Bob\'s Number Y:', self.y_entry.get())

        start = time.time()
        result = generate_symmetric_key(
            int(self.n_entry.get()),
            int(self.g_entry.get()),
            int(self.x_entry.get()),
            int(self.y_entry.get())
        )
        print('Key Generation Finished!')
        done = time.time()
        elapsed = done - start
        size = len(str(result))

        title = 'Finish Diffie-Hellman Session Key Generation'
        self.controller.show_end_frame(title, '', result, True, elapsed, size)
