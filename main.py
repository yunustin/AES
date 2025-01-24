from tkinterdnd2 import TkinterDnD
from gui import AESApp
import os

#Dnd kütüphanesi için, ellemeyin -Y
os.environ["TKDND_LIBRARY"] = r"C:\Python39\tcl\tkdnd2.9"

if __name__ == "__main__":
    app = TkinterDnD.Tk()
    gui = AESApp(app)
    app.mainloop()