import os
import time
import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.rsa.main import generate_pair, encrypt, decrypt


class RSAForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Algoritma RSA')

        self.render_mode_frame()
        self.render_message_option_frame()
        self.render_message_frame()
        self.render_message_type_frame()
        self.render_selected_key_frame()
        self.render_execute_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.MODE_ROW = 1
        self.MESSAGE_OPTION_ROW = 2
        self.MESSAGE_ROW = 3
        self.OUTPUT_ROW = 4
        self.KEY_OPTION_ROW = 5
        self.EXECUTE_ROW = 6

        self.encrypt = tk.IntVar()
        self.encrypt.set(0)

        self.message_option = tk.IntVar()
        self.message_option.set(0)

        self.key_option = tk.IntVar()
        self.key_option.set(0)
        
        self.message_dir = tk.StringVar()
        self.message_dir.set('')

        self.output_dir = tk.StringVar()
        self.output_dir.set('')

    def render_mode_frame(self):
        mode_frame = hg.create_frame(self, self.MODE_ROW + 1)

        hg.create_label(mode_frame, 'Metode:', 0, 0)
        hg.create_radio_button(
            mode_frame, 'Encrypt', 0, self.encrypt, 1, 0, None)
        hg.create_radio_button(
            mode_frame, 'Decrypt', 1, self.encrypt, 1, 1, None)

    def render_message_option_frame(self):
        message_option_frame = hg.create_frame(self, self.MESSAGE_OPTION_ROW + 1)

        hg.create_label(message_option_frame, 'Message Input:', 0, 0)
        hg.create_radio_button(
            message_option_frame, 'Type', 0, self.message_option, 1, 0, self.render_message_type_frame)
        hg.create_radio_button(
            message_option_frame, 'Select File', 1, self.message_option, 1, 1, self.render_message_file_frame)

    def render_message_frame(self):
        self.message_frame = hg.create_frame(self, self.MESSAGE_ROW + 1)
        self.output_frame = hg.create_frame(self, self.OUTPUT_ROW + 1)

        hg.create_label(self.message_frame, 'Message', 0, 0)

    def destroy_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def render_message_type_frame(self):
        self.destroy_frame(self.message_frame)
        self.destroy_frame(self.output_frame)
        
        self.render_message_frame()

        self.message_entry = hg.create_entry(self.message_frame, "", 1, 0)

    def render_message_file_frame(self):
        self.destroy_frame(self.message_frame)
        self.destroy_frame(self.output_frame)

        self.render_message_frame()
        self.render_output_frame()

        hg.create_label(self.message_frame, self.message_dir, 0, 1, fix_text=False)
        hg.create_button(self.message_frame, 'Choose',
                        lambda: self.load_message(), 1, 0)

    def render_output_frame(self):
        hg.create_label(self.output_frame, 'Output', 0, 0)
        self.output_dir = hg.create_entry(self.output_frame, "", 1, 0)
        hg.create_label(self.output_frame, '.txt', 1, 1)

    def render_selected_key_frame(self):
        selected_key_frame = hg.create_frame(self, self.KEY_OPTION_ROW + 1)

        hg.create_label(selected_key_frame, 'Selected Key:', 0, 0)
        self.selected_key_entry = hg.create_entry(selected_key_frame, "", 1, 0)
        hg.create_button(selected_key_frame, 'Choose',
                lambda: self.load_selected_key(), 2, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def load_message(self):
        dialog = fd.askopenfilename()
        self.message_dir.set(dialog)

    def load_selected_key(self):
        dialog = fd.askopenfilename()
        fo = open(dialog, 'r')
        lines = fo.read()
        fo.close()

        self.selected_key_entry.delete(0, tk.END)
        self.selected_key_entry.insert(tk.END, lines)

    def generate_key(self):
        print('GENERATE KEY FOR RSA ALGORITHM')
        generate_pair(self.public_key_dir.get(), self.private_key_dir.get())

    def execute(self):
        print('RSA {} Started!'.format("Encrypt" if self.encrypt.get() == 0 else "Decrypt"))
        if (self.message_option.get() == 0):
            print('> Message:', self.message_entry.get())
        else:
            print('> Message dir:', self.message_dir.get())
            print('> Output dir:', self.output_dir.get())

        print('> Key:', self.selected_key_entry.get())

        message = ""
        if (self.message_option.get() == 0):
            message = self.message_entry.get()
        else:
            mesage_dir = self.message_dir.get()
            fo = open(mesage_dir, 'r')
            message = fo.read()
            fo.close() 

        key = self.selected_key_entry.get()

        if message == '' or key == '':
            return

        start = time.time()

        if (self.encrypt.get() == 0):
            result = encrypt(message, key)
        else:
            result = decrypt(message, key)
        
        done = time.time()
        elapsed = done - start
        size = 0
        
        output_dir = ""

        if (self.message_option.get() == 1):
            output_dir = "output/" + self.output_dir.get() + ".txt"

            f = open(output_dir, "w")
            f.write(result)
            f.close()
            
            size = os.path.getsize(output_dir)

        print('{} Finished!'.format("Encrypt" if self.encrypt.get() == 0 else "Decrypt"))
        
        title = "Finish {} with RSA".format("Encrypt" if self.encrypt.get() == 0 else "Decrypt")
        self.controller.show_end_frame(title, output_dir, result, self.message_option.get() == 0, elapsed, size)
