import os
import json
from pathlib import Path
from tkinter import Tk, Label, Entry, Button
from tkinter import S, W, E, N, END, messagebox

class App():

    DEFPAD=(10,10)
    txt_gs = None
    txt_source = None
    txt_dest = None

    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    conf_path = os.path.join(current_directory, "conf.json")

    def __init__(self):
        self.setup_components()
        self.read_json()

    def setup_components(self):
        self.window=Tk()
        # GhostScript Path
        lbl_gs = Label(self.window, text="GhostScript Path")
        lbl_gs.grid(row=0, column=0, columnspan=1, sticky=N+W, padx=self.DEFPAD, pady=self.DEFPAD)

        self.txt_gs = Entry(self.window)
        self.txt_gs.grid(row=0, column=1, columnspan=4, sticky=N+W+E, padx=self.DEFPAD, pady=self.DEFPAD)

        # Source Dir
        lbl_source = Label(self.window, text="Source Path")
        lbl_source.grid(row=1, column=0, columnspan=1, sticky=N+W, padx=self.DEFPAD, pady=self.DEFPAD)

        self.txt_source = Entry(self.window)
        self.txt_source.grid(row=1, column=1, columnspan=4, sticky=N+W+E, padx=self.DEFPAD, pady=self.DEFPAD)

        # Destination Dir
        lbl_dest = Label(self.window, text="Destination Path")
        lbl_dest.grid(row=2, column=0, columnspan=1, sticky=N+W, padx=self.DEFPAD, pady=self.DEFPAD)

        self.txt_dest = Entry(self.window)
        self.txt_dest.grid(row=2, column=1, columnspan=4, sticky=N+W+E, padx=self.DEFPAD, pady=self.DEFPAD)

        btn = Button(self.window, text="Save", command=self.save)
        btn.grid(row=3, column=1, columnspan=4, sticky=S+W+E, padx=self.DEFPAD, pady=self.DEFPAD)

        # Window Properties
        self.window.title('Convert PDF/A Config Tool')
        self.window.geometry("640x480+10+20")
        self.window.grid_columnconfigure(4, weight=1)
        self.window.grid_rowconfigure(4, weight=1)

    def save(self):
        json_data = {
            'gs_executable': self.txt_gs.get(),
            'source_dir': self.txt_source.get(),
            'destination_dir': self.txt_dest.get()
        }

        try:
            with open(self.conf_path, encoding='utf-8', mode='w') as json_file:
                json.dump(json_data, json_file)
                messagebox.showinfo(title='Success', message='Configuration file saved')
        except:
                messagebox.showerror(title='Error', message='Error while saving the conf file')


    def set_text(self, text, component):
        component.delete(0, END)
        component.insert(0, text)
        return component

    def read_json(self):
        try:
            with open(self.conf_path, encoding='utf-8') as json_file:
                data = json.load(json_file)
                self.txt_gs = self.set_text(r"{}".format(data['gs_executable']), self.txt_gs)
                self.txt_source = self.set_text(Path(data['source_dir']), self.txt_source)
                self.txt_dest = self.set_text(Path(data['destination_dir']), self.txt_dest)
        except:
                self.txt_gs = self.set_text("", self.txt_gs)
                self.txt_source = self.set_text("", self.txt_source)
                self.txt_dest = self.set_text("", self.txt_dest)


app = App()
app.window.mainloop()