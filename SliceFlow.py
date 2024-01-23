import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import tkinter as tk
from tkinter import Label, Entry, Button, filedialog

class VideoSplitterGUI:
    def __init__(self, master):
        self.master = master
        master.title("Video Splitter")
        master.geometry("400x300")  # Set the size to 10x10 centimeters

        self.label_duration = Label(master, text="Enter the duration for each video (MM:SS):", pady=10)
        self.label_duration.pack()

        self.entry_duration = Entry(master)
        self.entry_duration.pack()

        self.label_output = Label(master, text="Specify output folder and base name:", pady=10)
        self.label_output.pack()

        self.entry_output = Entry(master)
        self.entry_output.pack()

        self.label_num_videos = Label(master, text="Enter the number of output videos:", pady=10)
        self.label_num_videos.pack()

        self.entry_num_videos = Entry(master)
        self.entry_num_videos.pack()

        self.add_file_button = Button(master, text="Add File", command=self.browse_file, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.add_file_button.pack()

        self.split_button = Button(master, text="Split Video", command=self.split_video, bg="#008CBA", fg="white", padx=10, pady=5)
        self.split_button.pack()

        self.file_path = ""

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mkv")])
        if file_path:
            self.file_path = file_path
            self.label_duration.config(text=f"Selected File: {os.path.basename(file_path)}", fg="blue")

    def parse_duration(self, duration_str):
        try:
            parts = list(map(int, duration_str.split(":")))
            if len(parts) == 2:
                return parts[0] * 60 + parts[1]
            elif len(parts) == 1:
                return parts[0]
        except ValueError:
            pass
        return None

    def split_video(self):
        if not self.file_path:
            self.label_duration.config(text="Please select a video file.", fg="red")
            return

        duration_str = self.entry_duration.get()
        num_videos_str = self.entry_num_videos.get()

        duration = self.parse_duration(duration_str)

        if duration is None or duration <= 0:
            self.label_duration.config(text="Invalid duration. Please enter a valid duration.", fg="red")
            return

        try:
            num_videos = int(num_videos_str)
        except ValueError:
            self.label_duration.config(text="Invalid input. Please enter a valid number of videos.", fg="red")
            return

        output_folder = self.entry_output.get()

        if not output_folder:
            self.label_duration.config(text="Please specify an output folder.", fg="red")
            return

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        clip = VideoFileClip(self.file_path)

        for i in range(num_videos):
            start_time = i * duration
            end_time = (i + 1) * duration
            output_path = os.path.join(output_folder, f"{self.entry_output.get()}_{i + 1}.mp4")
            ffmpeg_extract_subclip(self.file_path, start_time, end_time, targetname=output_path)

        self.label_duration.config(text="Video split successfully.", fg="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoSplitterGUI(root)
    root.mainloop()
