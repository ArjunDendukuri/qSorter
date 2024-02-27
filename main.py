import os
from os import path, listdir, mkdir, makedirs, replace, remove, name
from tkinter import Tk, Label, StringVar, Entry, Event
from shutil import copy2

from PIL import ImageTk, Image

folder = ""
out = "out"
sep = "\\" if os.name == "nt" else "/"

select: int
root: Tk
img_label: Label
indicator_label: Label

images: list[str]
img: ImageTk.PhotoImage
chapter_name: StringVar

chapters: list[str]
code: str


def tkcreate():
    global root, img, img_label, chapter_name, select, indicator_label
    root = Tk()
    chapter_name = StringVar()

    select = 0

    img = ImageTk.PhotoImage(Image.open(images[select]))
    root.geometry(f'{img.width() + 50}x{img.height() + 150}')

    img_label = Label(image=img)
    img_label.grid(row=0, column=0, columnspan=2, padx=25, pady=20)

    indicator_label = Label(text="Press ENTER to go to the next q", font=("Verdana", 20))
    indicator_label.grid(row=10, column=0, columnspan=2, padx=25, pady=8)
    text_box = Entry(root, textvariable=chapter_name, width=50)
    text_box.grid(row=11, column=0, columnspan=2, padx=25, pady=8)

    next_img()
    root.bind("<Key>", key_in)
    root.mainloop()


def key_in(key: Event):
    global images, select
    if key.keycode == (13 if sep == "\\" else 603979789):
        if finish():
            select = min(len(images), select + 1)
            next_img()


def finish() -> bool:
    global chapter_name, chapters
    img_name = images[select].split(sep)[-1]

    chapy = chapter_name.get()

    if len(chapy.split(",")) > 1:
        answer_png_name: str | None = None
        for chS in chapy.split(","):
            ch = chS.strip()
            if ch not in chapters:
                indicator_label.config(text="Invalid chapter", fg="#c70202", font=("Verdana", 20))
                return False
            else:
                copy2(f"{images[select]}", f"{out}{sep}{code}{sep}{ch}{sep}questions{sep}{img_name}")

                try:
                    if not answer_png_name:
                        a_name_list = list(images[select].split(sep)[-1])
                        if not a_name_list[-6].isnumeric():
                            a_name_list[-6] = 'A'
                        else:
                            a_name_list[-7] = 'A'
                        answer_png_name = "".join(a_name_list)

                    copy2(f"{folder}{sep}answers{sep}{answer_png_name}",
                          f"{out}{sep}{code}{sep}{ch}{sep}answers{sep}{answer_png_name}")

                except (FileNotFoundError, NotImplementedError):
                    print(f"Failed to move answer ({images[select]})")

        remove(images[select])
        remove(f"{folder}{sep}answers{sep}{answer_png_name}")
        chapter_name.set("")
        indicator_label.config(text="Press enter to go to next", fg="#000000", font=("Verdana", 20))
        return True

    # ~~~~~~~~
    if not chapy:
        indicator_label.config(text="Enter a chapter name fool", fg="#c70202", font=("Verdana", 20))
        return False
    elif chapy not in chapters and not chapy.lower() == "s":
        indicator_label.config(text="Invalid chapter", fg="#c70202", font=("Verdana", 20))
        return False

    if not chapy.lower() == "s":
        replace(f"{images[select]}", f"{out}{sep}{code}{sep}{chapy}{sep}questions{sep}{img_name}")  # moves question

        try:
            a_name_list = list(images[select].split(sep)[-1])
            if not a_name_list[-6].isnumeric():
                a_name_list[-6] = 'A'
            else:
                a_name_list[-7] = 'A'
            answer_png_name = "".join(a_name_list)

            replace(f"{folder}{sep}answers{sep}{answer_png_name}",
                    f"{out}{sep}{code}{sep}{chapy}{sep}answers{sep}{answer_png_name}")  # moves answer
        except (NotImplementedError, FileNotFoundError):
            print(f"Failed to move answer ({images[select]})")
    else:
        remove(images[select])

    chapter_name.set("")
    indicator_label.config(text="Press enter to go to next", fg="#000000", font=("Verdana", 20))
    return True


def next_img():
    global img, select, root, images, img_label

    if len(images) == select:
        root.destroy()
        print(f"All files complete! Thank you for your service, {folder}")
        return

    img = ImageTk.PhotoImage(Image.open(images[select]))
    root.geometry(f'{img.width() + 50}x{img.height() + 150}')
    img_label.config(image=img)


def handle_chapter_dirs():
    global code, chapters
    code = input("Enter subject code (with initial 0; 0606 not 606)\n")
    print("Enter chapter dirs seperated by a (,)")
    chapter_names = input("Example: 1,2,3 or A1,A2,B2\n")
    chapters = [ch.strip() for ch in chapter_names.split(",") if ch.strip()]

    for ch in chapters:
        if not path.exists(f"{out}{sep}{code}{sep}{ch}{sep}questions"):
            makedirs(f"{out}{sep}{code}{sep}{ch}{sep}questions")

        if not path.exists(f"{out}{sep}{code}{sep}{ch}{sep}answers"):
            makedirs(f"{out}{sep}{code}{sep}{ch}{sep}answers")


if __name__ == "__main__":
    folder = input('Enter your name\n').upper()
    try:
        images = [f"{folder}{sep}questions{sep}{img_path}" for img_path in listdir(f"{folder}{sep}questions")
                  if
                  path.isfile(f"{folder}{sep}questions{sep}{img_path}") and path.splitext(f"{folder}{sep}questions{sep}{img_path}")[
                      1] == ".png"]

        if not path.exists(f"{folder}{sep}answers"):
            raise FileNotFoundError()
    except FileNotFoundError:
        print("Improper file structure")
        exit(0)

    if len(images) == 0:
        print("No images found!")
        exit(0)

    if not path.exists(out):
        mkdir(out)

    handle_chapter_dirs()
    print("INSTRUCTIONS:")
    print("Enter chapters in textbox")
    print("If multiple seperate them with a comma")
    print("If the question is outdated/isn't in the syllabus anymore enter 's' as the chapter")
    input(f"Press enter to begin, {folder}")
    tkcreate()
