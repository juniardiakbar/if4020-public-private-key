import tkinter as tk
import src.helper.gui as hg


class EndPage(tk.Frame):
    def __init__(self, parent, controller, title, file_dir, result, isTyping, time, size):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text=title,
            font='none 24 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        output_frame = hg.create_frame(self, 2)
        hg.create_label(output_frame, 'Result:', 0, 0)
        
        if (not isTyping):
            hg.create_label(output_frame, file_dir, 0, 1)
        else:
            hg.create_label(output_frame, result, 1, 0)

        info_frame = hg.create_frame(self, 3)
        hg.create_label(info_frame, 'Time elapsed: ' + str(time), 0, 0)
        hg.create_label(info_frame, 'Size: ' + str(size), 1, 0)

        back_frame = hg.create_frame(self, 4)
        hg.create_button(back_frame, 'Back',
                        lambda: self.controller.show_frame("StartPage"), 0, 1)
        
