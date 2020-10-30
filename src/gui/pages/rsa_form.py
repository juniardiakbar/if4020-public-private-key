import tkinter as tk
import tkinter.filedialog as fd
import src.helper.gui as hg

from src.rsa.main import generate_pair
# from src.audio.psnr import audio_PSNR
# from src.helper.file import File


class RSAForm(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller
        self.initialize()

        hg.insert_header(self, 'Algoritma RSA')

        self.render_key_frame()
        self.render_mode_frame()
        self.render_message_option_frame()
        self.render_message_frame()
        self.render_key_option_frame()
        # self.render_key_frame()
        # self.render_options_frame()
        # self.render_output_frame()
        # self.render_execute_frame()

    def initialize(self):
        self.TITLE_ROW = 0
        self.PUBLIC_KEY_ROW = 1
        self.PRIVATE_KEY_ROW = 2
        self.BUTTON_KEY_ROW = 3
        self.MODE_ROW = 4
        self.MESSAGE_OPTION_ROW = 5
        self.MESSAGE_ROW = 6
        self.KEY_OPTION_ROW = 7
        self.KEY_ROW = 8

        self.DEFAULT_OUT_FILENAME = 'insert_result'

        self.encrypt = tk.IntVar()
        self.encrypt.set(0)

        self.message_option = tk.IntVar()
        self.message_option.set(0)

        self.key_option = tk.IntVar()
        self.key_option.set(0)
        
        self.random = tk.IntVar()
        self.random.set(0)

        self.audio_dir = tk.StringVar()
        self.audio_dir.set('')

        self.public_key_dir = tk.StringVar()
        self.public_key_dir.set('')

        self.private_key_dir = tk.StringVar()
        self.private_key_dir.set('')

        self.message_dir = tk.StringVar()
        self.message_dir.set('')

        self.output_filename = tk.StringVar()
        self.output_filename.set(self.DEFAULT_OUT_FILENAME)

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
        hg.create_button(button_key_frame, 'Generate Key (optional)',
                    lambda: self.generate_key(), 1, 0)

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
            message_option_frame, 'Type', 0, self.message_option, 1, 0, self.on_select_message_frame())
        hg.create_radio_button(
            message_option_frame, 'Select File', 1, self.message_option, 1, 1, self.on_select_message_frame())

    def on_select_message_frame(self):
        print(self.message_option.get())

    def render_message_frame(self):
        message_frame = hg.create_frame(self, self.MESSAGE_ROW + 1)

        if (self.message_option.get() == 0):
            hg.create_label(message_frame, 'Message Type', 0, 0)
        else :
            hg.create_label(message_frame, 'Message', 0, 0)
            hg.create_label(message_frame, self.message_dir, 0, 1, fix_text=False)
            hg.create_button(message_frame, 'Choose',
                            lambda: self.load_secret_message(), 1, 0)

    def render_key_option_frame(self):
        key_option_frame = hg.create_frame(self, self.KEY_OPTION_ROW + 1)

        hg.create_label(key_option_frame, 'Key Option:', 0, 0)
        hg.create_radio_button(
            key_option_frame, 'Type', 0, self.key_option, 1, 0, None)
        hg.create_radio_button(
            key_option_frame, 'Select File', 1, self.key_option, 1, 1, None)

    # def render_key_frame(self):
    #     key_frame = hg.create_frame(self, self.KEY_ROW + 1)

    #     hg.create_label(key_frame, 'Stegano Key:', 0, 0)
    #     self.key_entry = hg.create_entry(key_frame, "", 1, 0)

    def render_options_frame(self):
        option_frame = hg.create_frame(self, self.OPTIONS_ROW + 1)

        hg.create_label(option_frame, 'Option:', 0, 0)
        hg.create_check_button(
            option_frame, 'Encrypt Message', self.encrypt, 1, 0)
        hg.create_check_button(
            option_frame, 'Random Frame', self.random, 1, 1)

    def render_output_frame(self):
        output_frame = hg.create_frame(self, self.OUTPUT_ROW + 1)

        hg.create_label(output_frame, 'Output file\'s name:', 0, 0)
        hg.create_label(output_frame, '.wav', 1, 1)
        self.output_name = hg.create_entry(
            output_frame, self.DEFAULT_OUT_FILENAME, 1, 0)

    def render_execute_frame(self):
        execute_frame = hg.create_frame(self, self.EXECUTE_ROW + 1)

        hg.create_button(execute_frame, 'Execute',
                         lambda: self.execute(), 0, 0)

        hg.create_button(execute_frame, 'Back',
                         lambda: self.controller.show_frame("StartPage"), 0, 1)

    def load_public_key(self):
        dialog = fd.askopenfilename()
        self.public_key_dir.set(dialog)

    def load_private_key(self):
        dialog = fd.askopenfilename()
        self.private_key_dir.set(dialog)

    def generate_key(self):
        print('GENERATE KEY FOR RSA ALGORITHM')
        generate_pair(self.public_key_dir.get(), self.private_key_dir.get())

    def load_secret_message(self):
        self.message_dir.set(fd.askopenfilename())

    def execute(self):
        print('Insertion Started!')
        print('> Audio dir:', self.audio_dir.get())
        print('> Message dir:', self.message_dir.get())
        print('> Key:', self.key_entry.get())
        print('> Random:', self.random.get())
        print('> Encrypt:', self.encrypt.get())

        file_dir = self.audio_dir.get()
        message_dir = self.message_dir.get()
        key = self.key_entry.get()
        output_filename = self.output_name.get()

        try:
            if file_dir == '' or message_dir == '' or key == '' or output_filename == '':
                return

            insert = Inserter(file_dir, message_dir, key)

            frame_modified = insert.insert_message(
                randomize=self.random.get(),
                encrypted=self.encrypt.get(),
            )

            file_name = "output/" + output_filename + ".wav"
            output_file = File(file_name)
            output_file.write_audio_file(frame_modified, insert.params)

            print('Insertion Finished!')

            modified_buff = output_file.init_buff_audio_file()
            psnr = audio_PSNR(insert.init_buff, modified_buff)
            title = "Finish Insert Secret Message to Audio"
            self.controller.show_end_frame(title, "Audio", file_name, psnr)

        except Exception as e:
            print("Error occured while insert secret message")
            print(e)
