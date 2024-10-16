try:
    from PIL import ImageTk, Image
except ImportError:
    print("Pillow is not installed. Please install it using 'pip install Pillow'.")
    exit(1)

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
from gtts import gTTS
import pyttsx3
import os

# Initialize pyttsx3 engine
engine = pyttsx3.init()

# Function to convert text to speech using pyttsx3 (offline)
def pyttsx3_speak(text, voice_gender, rate):
    try:
        # Set properties
        voices = engine.getProperty('voices')
        if voice_gender == "Male":
            engine.setProperty('voice', voices[0].id)
        else:
            engine.setProperty('voice', voices[1].id)

        engine.setProperty('rate', rate)
        print(f"Speaking (pyttsx3): {text}")  # Debug print
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to speak text: {str(e)}")

# Function to convert text to speech using gTTS (online)
def gtts_speak(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        file_path = "speech.mp3"
        tts.save(file_path)
        print(f"Playing (gTTS): {text}")  # Debug print
        os.system(f"start {file_path}")  # For Windows, use 'xdg-open' for Linux
    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert text to speech: {str(e)}")

# Function to save the speech as an MP3 or WAV file
def save_speech(text, lang='en', file_format="mp3"):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        file_extension = f".{file_format}"
        save_path = filedialog.asksaveasfilename(defaultextension=file_extension, filetypes=[(f"{file_format.upper()} files", f"*.{file_format}")])
        if save_path:
            tts.save(save_path)
            messagebox.showinfo("Success", f"Speech saved as {file_format.upper()} file successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save speech: {str(e)}")

# Function to load text from a file
def load_text(text_entry):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            text_entry.delete(1.0, tk.END)
            text_entry.insert(tk.END, file.read())

# UI Setup
def create_ui():
    # Create the root window with ttkbootstrap style
    root = ttk.Window(themename="flatly")
    root.title("Styled Text-to-Speech App")
    root.geometry("600x500")

    # Add widgets with ttkbootstrap
    text_label = ttk.Label(root, text="Enter Text:", bootstyle="primary")
    text_label.pack(pady=10)
    
    text_entry = ttk.Text(root, height=8, width=60)
    text_entry.pack(pady=10)
    
    # Voice gender option
    voice_label = ttk.Label(root, text="Select Voice:", bootstyle="secondary")
    voice_label.pack(pady=5)
    voice_var = ttk.StringVar(value="Male")
    male_radio = ttk.Radiobutton(root, text="Male", variable=voice_var, value="Male", bootstyle="info")
    female_radio = ttk.Radiobutton(root, text="Female", variable=voice_var, value="Female", bootstyle="info")
    male_radio.pack(pady=2)
    female_radio.pack(pady=2)

    # Speech rate option
    rate_label = ttk.Label(root, text="Speech Rate:", bootstyle="secondary")
    rate_label.pack(pady=5)
    rate_scale = ttk.Scale(root, from_=100, to=300, orient="horizontal", bootstyle="info")
    rate_scale.set(150)  # Default rate
    rate_scale.pack(pady=5)

    # Language selection for gTTS
    lang_label = ttk.Label(root, text="Select Language for Online Speech:", bootstyle="secondary")
    lang_label.pack(pady=5)
    lang_var = ttk.StringVar(value="en")
    lang_menu = ttk.Combobox(root, textvariable=lang_var, values=["en", "es", "fr", "de", "zh", "hi", "ar", "ru"], bootstyle="info")
    lang_menu.pack(pady=5)
    lang_menu.set("en")  # Default to English

    # File format selection for saving
    format_label = ttk.Label(root, text="Select File Format:", bootstyle="secondary")
    format_label.pack(pady=5)
    format_var = ttk.StringVar(value="mp3")
    format_menu = ttk.Combobox(root, textvariable=format_var, values=["mp3", "wav"], bootstyle="info")
    format_menu.pack(pady=5)

    # Function for Speak Button
    def speak():
        text = text_entry.get("1.0", tk.END).strip()
        voice = voice_var.get()
        rate = rate_scale.get()
        if text:
            pyttsx3_speak(text, voice, rate)
        else:
            messagebox.showwarning("Warning", "Please enter some text to speak.")

    # Function for gTTS speak
    def gtts_speak_function():
        text = text_entry.get("1.0", tk.END).strip()
        lang = lang_var.get()
        if text:
            gtts_speak(text, lang)
        else:
            messagebox.showwarning("Warning", "Please enter some text to speak.")

    # Function to save speech as file
    def save_file():
        text = text_entry.get("1.0", tk.END).strip()
        lang = lang_var.get()
        file_format = format_var.get()
        if text:
            save_speech(text, lang, file_format)
        else:
            messagebox.showwarning("Warning", "Please enter some text to save.")

    # Load text from file
    load_button = ttk.Button(root, text="Load Text from File", command=lambda: load_text(text_entry), bootstyle="primary-outline")
    load_button.pack(pady=5)

    # Speak Button
    speak_button = ttk.Button(root, text="Speak (Offline)", command=speak, bootstyle="success")
    speak_button.pack(pady=10)

    # gTTS Speak Button
    gtts_button = ttk.Button(root, text="Speak (Online)", command=gtts_speak_function, bootstyle="warning")
    gtts_button.pack(pady=5)

    # Save Button
    save_button = ttk.Button(root, text="Save as File", command=save_file, bootstyle="danger-outline")
    save_button.pack(pady=5)

    # Clear Text Button
    clear_button = ttk.Button(root, text="Clear Text", command=lambda: text_entry.delete(1.0, tk.END), bootstyle="secondary-outline")
    clear_button.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
