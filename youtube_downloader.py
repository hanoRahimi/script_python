import tkinter as tk
from tkinter.filedialog import askdirectory
from pytube import YouTube
from tkinter import messagebox

window=tk.Tk()
window.title("Youtube Downloader")
window.minsize(500,200)

def widgets():
    link_label = tk.Label(window, text="Video Link")
    link_label.grid(row=0, column=0, padx=20, pady=20)
    link_label.config(font=("None", 15), fg="red")

    link_input = tk.Entry(window, width=40, textvariable=video_link)
    link_input.grid(row=0, column=1)

    place_label = tk.Label(window, text="Directory")
    place_label.grid(row=1, column=0, sticky="w", padx=20, pady=20)
    place_label.config(font=("None", 15), fg="red")

    place_input = tk.Entry(window, width=40, textvariable=download_dir)
    place_input.grid(row=1, column=1, sticky="w")

    place_btn = tk.Button(window, text="Open", width=10, bg="black", fg="white", command=browse_folder)
    place_btn.grid(row=1, column=2, padx=20)

    download_btn = tk.Button(window, text="Download Now", fg="white", bg="black", font=("None", 20), padx=10, command=download)
    download_btn.grid(row=2, column=1)


def browse_folder():
    directory= askdirectory(initialdir="YOUR DIRECTORY PATH", title="save")
    download_dir.set(directory)

def download():
    link= video_link.get()
    save_dir=download_dir.get()
    yt=YouTube(link)
    yt.streams.first().download(save_dir)
    messagebox.showinfo(title="Success",message="Your Video Download Successfully!")

download_dir= tk.StringVar()
video_link=tk.StringVar()


widgets()

window.mainloop()
