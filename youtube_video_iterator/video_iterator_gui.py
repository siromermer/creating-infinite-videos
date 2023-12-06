import tkinter as tk
from pytube import YouTube
from moviepy.editor import VideoFileClip, concatenate_videoclips
from PIL import Image, ImageTk

def video_indir():
    video_linki = entry_link.get()
    try:
        yt = YouTube(video_linki)
        video = yt.streams.get_highest_resolution()
        video.download(filename="desired_video.mp4")
        label_sonuc.config(text="succesfully downloaded")
    except Exception as e:
        label_sonuc.config(text="cant download")

def saat_ayarla():
    try:
        saat = int(entry_saat.get())
        label_sonuc.config(text=f"hour: {saat}")
        iterate_video(saat)
    except ValueError:
        label_sonuc.config(text="not valid hour")

def iterate_video(hour_duration):
    video = VideoFileClip("desired_video.mp4")
    length_of_video = video.duration
    hour_to_second = hour_duration * 60 * 60
    iteration = hour_to_second / length_of_video
    concatenated_video = video

    for i in range(int(iteration)):
        concatenated_video = concatenate_videoclips([concatenated_video, video])

    concatenated_video.write_videofile(f"iteratedvideo{hour_duration}hour.mp4")

def play_downloaded_video():
    try:
        video_path = "desired_video.mp4"
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(0)

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)

        label_video.config(image=img_tk)
        label_video.image = img_tk

        def update_frame(idx):
            frame = clip.get_frame(idx / clip.fps)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            label_video.config(image=img_tk)
            label_video.image = img_tk
            label_video.after(33, update_frame, (idx + 1) % int(clip.fps * clip.duration))

        update_frame(0)

    except Exception as e:
        print(f"Hata: {e}")

root = tk.Tk()
root.title("YouTube Video ve Saat Ayarlama")
root.geometry("650x600")

label_link = tk.Label(root, text="Youtube Link")
label_link.pack()
entry_link = tk.Entry(root, width=50)
entry_link.pack(pady=10)

label_saat = tk.Label(root, text="Hour")
label_saat.pack()
entry_saat = tk.Entry(root)
entry_saat.pack(pady=10)

button_indir = tk.Button(root, text="Download video", command=video_indir)
button_indir.pack(pady=10)

label_sonuc = tk.Label(root, text="")
label_sonuc.pack()

button_play = tk.Button(root, text="play original video", command=play_downloaded_video)
button_play.pack()

button_saat_ayarla = tk.Button(root, text="Give me extended video", command=saat_ayarla)
button_saat_ayarla.pack(pady=10)

label_video = tk.Label(root, width=500, height=300, padx=10)
label_video.pack( pady=20)

 

root.mainloop()
