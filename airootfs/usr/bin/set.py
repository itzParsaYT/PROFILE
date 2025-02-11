import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import sv_ttk as s
import darkdetect
import os

class SettingsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leily Settings Editor")
        self.root.geometry("1000x600")
        
        # Set theme based on system preference
        if darkdetect.isDark():
            s.set_theme("dark")
        elif darkdetect.isLight():
            s.set_theme("light")
        else:
            messagebox.showwarning("Warning", "We did not detect any valid value for the current theme variant.\nLeily Settings Editor will use the dark theme.")
            s.set_theme("dark")
        
        # Load JSON data
        self.original_json_data = self.load_json()
        self.json_data = self.original_json_data.copy()
        
        # Track the current section
        self.current_section = None
        
        # Create sidebar
        self.create_sidebar()
        
        # Create content area
        self.content_frame = ttk.Frame(root)
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create button frame at the bottom of the content area
        self.button_frame = ttk.Frame(self.content_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        
        # Add Save, Cancel, and Revert buttons
        ttk.Button(self.button_frame, text="Cancel", command=self.cancel_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.button_frame, text="Revert", command=self.revert_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(self.button_frame, text="Save", command=self.save_json).pack(side=tk.RIGHT, padx=5)
        
        # Initialize with the General section
        self.show_general_section()
    
    def load_json(self):
        # Load the JSON file (you can modify this to load from a file)
        return {
            "name": "Leily",
            "greeting": "Greetings!",
            "record-duration": 3,
            "channels": 2,
            "rate": 44100,
            "chunk-size": 1024,
            "notifications-enabled": False,
            "show-commands-on-startup": True,
            "logs": True,
            "speech-threshold": 2500,
            "live-mode": False,
            "use-hot-word-in-basic-mode": False,
            "hot-words": ["hey leily", "here leily", "listen leily"],
            "master-mode": False,
            "master-mode-barrier-speech-enabled": True,
            "master-mode-barrier-speech": "Unauthorized",
            "voice-pitch": 1.0,
            "voice-feedback-enabled": True,
            "voice-transcription-feedback-enabled": False,
            "voice-feedback-speed": 1.35,
            "voice-cache-enabled": True,
            "voice-feedback-default-speeches": [],
            "voice-feedback-transcription-capable-speeches": ["transcribing...", "getting it..."],
            "voice-feedback-turning-off": "Goodbye!"
        }
    
    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Sidebar buttons
        ttk.Button(sidebar, text="General", command=self.show_general_section).pack(fill=tk.X, pady=5)
        ttk.Button(sidebar, text="Audio", command=self.show_audio_section).pack(fill=tk.X, pady=5)
        ttk.Button(sidebar, text="Voice Feedback", command=self.show_voice_feedback_section).pack(fill=tk.X, pady=5)
        ttk.Button(sidebar, text="Master Mode", command=self.show_master_mode_section).pack(fill=tk.X, pady=5)
    
    def clear_content_frame(self):
        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            if widget != self.button_frame:  # Don't clear the button frame
                widget.destroy()
    
    def show_general_section(self):
        self.clear_content_frame()
        self.current_section = "General"
        
        # Section title
        ttk.Label(self.content_frame, text="General Settings", font=("Arial", 18)).pack(pady=10)
        
        # Name
        ttk.Label(self.content_frame, text="Name:").pack(padx=10, pady=5, anchor=tk.W)
        self.name_entry = ttk.Entry(self.content_frame)
        self.name_entry.insert(0, self.json_data["name"])
        self.name_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Greeting
        ttk.Label(self.content_frame, text="Greeting:").pack(padx=10, pady=5, anchor=tk.W)
        self.greeting_entry = ttk.Entry(self.content_frame)
        self.greeting_entry.insert(0, self.json_data["greeting"])
        self.greeting_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Notifications Enabled
        self.notifications_enabled = tk.BooleanVar(value=self.json_data["notifications-enabled"])
        ttk.Checkbutton(self.content_frame, text="Notifications Enabled", variable=self.notifications_enabled).pack(padx=10, pady=5, anchor=tk.W)
        
        # Show Commands on Startup
        self.show_commands_on_startup = tk.BooleanVar(value=self.json_data["show-commands-on-startup"])
        ttk.Checkbutton(self.content_frame, text="Show Commands on Startup", variable=self.show_commands_on_startup).pack(padx=10, pady=5, anchor=tk.W)
        
        # Logs
        self.logs = tk.BooleanVar(value=self.json_data["logs"])
        ttk.Checkbutton(self.content_frame, text="Enable Logs", variable=self.logs).pack(padx=10, pady=5, anchor=tk.W)
    
    def show_audio_section(self):
        self.clear_content_frame()
        self.current_section = "Audio"
        
        # Section title
        ttk.Label(self.content_frame, text="Audio Settings", font=("Arial", 18)).pack(pady=10)
        
        # Record Duration
        ttk.Label(self.content_frame, text="Record Duration:").pack(padx=10, pady=5, anchor=tk.W)
        self.record_duration_entry = ttk.Entry(self.content_frame)
        self.record_duration_entry.insert(0, self.json_data["record-duration"])
        self.record_duration_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Channels
        ttk.Label(self.content_frame, text="Channels:").pack(padx=10, pady=5, anchor=tk.W)
        self.channels_entry = ttk.Entry(self.content_frame)
        self.channels_entry.insert(0, self.json_data["channels"])
        self.channels_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Rate
        ttk.Label(self.content_frame, text="Rate:").pack(padx=10, pady=5, anchor=tk.W)
        self.rate_entry = ttk.Entry(self.content_frame)
        self.rate_entry.insert(0, self.json_data["rate"])
        self.rate_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Chunk Size
        ttk.Label(self.content_frame, text="Chunk Size:").pack(padx=10, pady=5, anchor=tk.W)
        self.chunk_size_entry = ttk.Entry(self.content_frame)
        self.chunk_size_entry.insert(0, self.json_data["chunk-size"])
        self.chunk_size_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Speech Threshold
        ttk.Label(self.content_frame, text="Speech Threshold:").pack(padx=10, pady=5, anchor=tk.W)
        self.speech_threshold_entry = ttk.Entry(self.content_frame)
        self.speech_threshold_entry.insert(0, self.json_data["speech-threshold"])
        self.speech_threshold_entry.pack(fill=tk.X, padx=10, pady=5)
    
    def show_voice_feedback_section(self):
        self.clear_content_frame()
        self.current_section = "Voice Feedback"
        
        # Section title
        ttk.Label(self.content_frame, text="Voice Feedback Settings", font=("Arial", 18)).pack(pady=10)
        
        # Voice Pitch
        ttk.Label(self.content_frame, text="Voice Pitch:").pack(padx=10, pady=5, anchor=tk.W)
        self.voice_pitch_entry = ttk.Entry(self.content_frame)
        self.voice_pitch_entry.insert(0, self.json_data["voice-pitch"])
        self.voice_pitch_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Voice Feedback Enabled
        self.voice_feedback_enabled = tk.BooleanVar(value=self.json_data["voice-feedback-enabled"])
        ttk.Checkbutton(self.content_frame, text="Voice Feedback Enabled", variable=self.voice_feedback_enabled).pack(padx=10, pady=5, anchor=tk.W)
        
        # Voice Feedback Speed
        ttk.Label(self.content_frame, text="Voice Feedback Speed:").pack(padx=10, pady=5, anchor=tk.W)
        self.voice_feedback_speed_entry = ttk.Entry(self.content_frame)
        self.voice_feedback_speed_entry.insert(0, self.json_data["voice-feedback-speed"])
        self.voice_feedback_speed_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Voice Cache Enabled
        self.voice_cache_enabled = tk.BooleanVar(value=self.json_data["voice-cache-enabled"])
        ttk.Checkbutton(self.content_frame, text="Voice Cache Enabled", variable=self.voice_cache_enabled).pack(padx=10, pady=5, anchor=tk.W)
    
    def show_master_mode_section(self):
        self.clear_content_frame()
        self.current_section = "Master Mode"
        
        # Section title
        ttk.Label(self.content_frame, text="Master Mode Settings", font=("Arial", 18)).pack(pady=10)
        
        # Master Mode
        self.master_mode = tk.BooleanVar(value=self.json_data["master-mode"])
        ttk.Checkbutton(self.content_frame, text="Master Mode", variable=self.master_mode).pack(padx=10, pady=5, anchor=tk.W)
        
        # Master Mode Barrier Speech Enabled
        self.master_mode_barrier_speech_enabled = tk.BooleanVar(value=self.json_data["master-mode-barrier-speech-enabled"])
        ttk.Checkbutton(self.content_frame, text="Master Mode Barrier Speech Enabled", variable=self.master_mode_barrier_speech_enabled).pack(padx=10, pady=5, anchor=tk.W)
        
        # Master Mode Barrier Speech
        ttk.Label(self.content_frame, text="Master Mode Barrier Speech:").pack(padx=10, pady=5, anchor=tk.W)
        self.master_mode_barrier_speech_entry = ttk.Entry(self.content_frame)
        self.master_mode_barrier_speech_entry.insert(0, self.json_data["master-mode-barrier-speech"])
        self.master_mode_barrier_speech_entry.pack(fill=tk.X, padx=10, pady=5)
    
    def save_json(self):
        # Update JSON data based on the current section
        if self.current_section == "General":
            self.json_data["name"] = self.name_entry.get()
            self.json_data["greeting"] = self.greeting_entry.get()
            self.json_data["notifications-enabled"] = self.notifications_enabled.get()
            self.json_data["show-commands-on-startup"] = self.show_commands_on_startup.get()
            self.json_data["logs"] = self.logs.get()
        elif self.current_section == "Audio":
            self.json_data["record-duration"] = int(self.record_duration_entry.get())
            self.json_data["channels"] = int(self.channels_entry.get())
            self.json_data["rate"] = int(self.rate_entry.get())
            self.json_data["chunk-size"] = int(self.chunk_size_entry.get())
            self.json_data["speech-threshold"] = int(self.speech_threshold_entry.get())
        elif self.current_section == "Voice Feedback":
            self.json_data["voice-pitch"] = float(self.voice_pitch_entry.get())
            self.json_data["voice-feedback-enabled"] = self.voice_feedback_enabled.get()
            self.json_data["voice-feedback-speed"] = float(self.voice_feedback_speed_entry.get())
            self.json_data["voice-cache-enabled"] = self.voice_cache_enabled.get()
        elif self.current_section == "Master Mode":
            self.json_data["master-mode"] = self.master_mode.get()
            self.json_data["master-mode-barrier-speech-enabled"] = self.master_mode_barrier_speech_enabled.get()
            self.json_data["master-mode-barrier-speech"] = self.master_mode_barrier_speech_entry.get()
        
        # Save to file
        file_path = os.getenv("HOME") + "/leily_cfg"
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.json_data, file, indent=4)
            messagebox.showinfo("Success", "Settings saved successfully!")
    
    def cancel_changes(self):
        self.root.destroy()
    
    def revert_changes(self):
        # Revert to the original JSON data
        res = messagebox.askquestion("Draft Changes", "Are you sure you want to revert the changes?")
        if res == "yes":
            self.json_data = self.original_json_data.copy()
            # Refresh the current section to show the original values
            if self.current_section == "General":
                self.show_general_section()
            elif self.current_section == "Audio":
                self.show_audio_section()
            elif self.current_section == "Voice Feedback":
                self.show_voice_feedback_section()
            elif self.current_section == "Master Mode":
                self.show_master_mode_section()
        else:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsApp(root)
    root.mainloop()