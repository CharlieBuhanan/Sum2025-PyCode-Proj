# Youtube Downloader Application
# Uses yt-dlp to download videos from YouTube

# TODO: Fix the customtkinter import issue

#import ffmpeg
import sys
import tkinter
import customtkinter as ctk # FIX THIS
import os
import subprocess
import shutil
from yt_dlp import YoutubeDL

def ensure_yt_dlp_installed():
    if shutil.which("ffmpeg") is None: # Check if ffmpeg is available
        print("ffmpeg is not installed or not in PATH")
    else:
        print("ffmpeg is available")

    # Check if yt_dlp is importable
    if shutil.which("yt-dlp") is None:
        print("yt-dlp not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
    else:
        print("yt-dlp is already installed.")
        
def get_video_filename(url, download_path):
    # Ask yt-dlp to tell us the output filename (dry-run)
    if audioOnly.get() == 1:
        result = subprocess.run([
        sys.executable, "-m", "yt_dlp",
        "--get-filename",
        "-x", "--audio-format", "mp3",
        "-o", "%(title)s [%(id)s].mp3",
        url
        ], stdout=subprocess.PIPE, text=True)
    else:
        result = subprocess.run([
            sys.executable, "-m", "yt_dlp",
            "--get-filename",
            "-o", "%(title)s [%(id)s].%(ext)s",
            url
        ], stdout=subprocess.PIPE, text=True)

    filename = result.stdout.strip()
    if len(filename) == 0:
        raise Exception("Failed to retrieve filename from yt-dlp. Check the URL.")
    
    ret = os.path.join(download_path, filename)
    print(f"Determined path/filename: {ret}") #DEBUGGING
    return ret

def startDownload():
    try:
        finishLabel.configure(text="Attempting Download... (This will take a couple seconds)", text_color="yellow")
        app.update_idletasks()

        ytlink = link.get().strip()
        download_path = os.path.join(os.path.expanduser("~"), "Downloads", "YoutubeDownloads")
        
        # Ensure yt-dlp is installed
        ensure_yt_dlp_installed()

        # Ensure the video file directory exists
        os.makedirs(download_path, exist_ok=True)
        print(download_path)

        # Get what the filename would be
        filepath = get_video_filename(ytlink, download_path)
        if os.path.exists(filepath):
            finishLabel.configure(text="File already exists!", text_color="yellow")
            return

        #Run yt-dlp command
        if audioOnly.get() == 1:
            # Audio download
            subprocess.run([
                sys.executable, "-m", "yt_dlp",
                "-x", "--audio-format", "mp3",
                "-P", download_path,
                "-o", "%(title)s [%(id)s].%(ext)s",  # consistent naming
                ytlink
            ])
        else:
            # Video download
            subprocess.run([
                sys.executable, "-m", "yt_dlp",
                "-P", download_path,
                ytlink
            ])

        finishLabel.configure(text="Download Successful!", text_color="green")
    except Exception as e:
        print(f"Error: {e}")
        finishLabel.configure(text=f"Download Failed.\n{e}", text_color="red")

if __name__ == "__main__":
    #Settings
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    # App Frame
    app = ctk.CTk()
    app.geometry("720x480")
    app.title("Youtube Downloader")

    # Adding UI Elements
    title = ctk.CTkLabel(app, text="Insert A YouTube Link", font=ctk.CTkFont(size=20, weight="bold"))
    title.pack(pady=12, padx=15)

    # User Input - Link
    url_var = tkinter.StringVar()
    link = ctk.CTkEntry(app, width=350, height=40, textvariable=url_var)
    link.pack()

    # Finish Label
    finishLabel = ctk.CTkLabel(app, text="Downloads will appear in: C:/Users/Name/Downloads/YoutubeDownloads", text_color="gray")
    finishLabel.pack(pady=12, padx=10)

    # Download Button Function
    download = ctk.CTkButton(app, text="Download", command=startDownload)
    download.pack(pady=15, padx=10)

    # Audio Only checkbox
    audioOnly = tkinter.IntVar()
    audio_checkbox = ctk.CTkCheckBox(app, text="Audio Only (webm)", variable=audioOnly)
    audio_checkbox.pack(pady=10)

    # Run App
    app.mainloop()
else:
    print("This module is not meant to be imported.")