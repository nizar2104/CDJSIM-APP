import customtkinter as ctk
import psutil
import os
import threading
import webbrowser  # Added this to open links
from tkinter import filedialog

# --- CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --- HARDWARE PROFILES ---
PROFILES = {
    # Multi Players
    "CDJ-2000NXS":  {"name": "CDJ-2000NXS",  "noFlac": True,  "exFat": False, "hfsPlus": True},
    "CDJ-2000NXS2": {"name": "CDJ-2000NXS2", "noFlac": False, "exFat": False, "hfsPlus": True},
    "CDJ-3000":     {"name": "CDJ-3000",     "noFlac": False, "exFat": True, "hfsPlus": True},
    "XDJ-1000MK2":  {"name": "XDJ-1000 MK2", "noFlac": False, "exFat": False, "hfsPlus": True},
    "XDJ-1000":     {"name": "XDJ-1000 MK1", "noFlac": True,  "exFat": False, "hfsPlus": True},
    "XDJ-700":      {"name": "XDJ-700",      "noFlac": True,  "exFat": False, "hfsPlus": True},
    
    # All-In-One Systems
    "XDJ-RR":       {"name": "XDJ-RR",       "noFlac": True,  "exFat": False, "hfsPlus": True},
    "XDJ-XZ":       {"name": "XDJ-XZ",       "noFlac": False, "exFat": False, "hfsPlus": True},
    "XDJ-RX3":      {"name": "XDJ-RX3",      "noFlac": False, "exFat": True, "hfsPlus": True},
    "OPUS-QUAD":    {"name": "OPUS-QUAD",    "noFlac": False, "exFat": True, "hfsPlus": True},
    "OMNIS-DUO":    {"name": "OMNIS-DUO",    "noFlac": False, "exFat": True, "hfsPlus": True},
    "XDJ-AZ":       {"name": "XDJ-AZ",       "noFlac": False, "exFat": True, "hfsPlus": True}
}

class CDJSimulatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("CDJ Simulator | By No-Mad")
        self.geometry("600x810") # Increased height for donation button
        self.resizable(False, False)

        # Variables
        self.selected_path = None

        # Container Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.label_title = ctk.CTkLabel(self.main_frame, text="CDJ SIMULATOR", 
                                      font=("Arial", 24, "bold"), text_color="white")
        self.label_title.pack(pady=(20, 0))

        self.label_author = ctk.CTkLabel(self.main_frame, text="BY NO-MAD", 
                                       font=("Arial", 12, "bold"), text_color="#0057e7")
        self.label_author.pack(pady=(0, 20))

        # 1. Select Gear
        self.lbl_gear = ctk.CTkLabel(self.main_frame, text="TARGET EQUIPMENT", text_color="#aaa")
        self.lbl_gear.pack(anchor="w", padx=30)
        
        self.gear_var = ctk.StringVar(value="CDJ-3000")
        self.gear_menu = ctk.CTkOptionMenu(self.main_frame, variable=self.gear_var,
                                         values=list(PROFILES.keys()),
                                         fg_color="#333", button_color="#0057e7")
        self.gear_menu.pack(pady=(5, 20), padx=30, fill="x")

        # 2. Select Drive Button
        self.lbl_drive = ctk.CTkLabel(self.main_frame, text="SELECT USB DRIVE", text_color="#aaa")
        self.lbl_drive.pack(anchor="w", padx=30)

        self.btn_browse = ctk.CTkButton(self.main_frame, text="📂 OPEN FINDER / SELECT DRIVE", 
                                      font=("Arial", 14, "bold"),
                                      height=40, fg_color="#333", hover_color="#444", 
                                      border_width=1, border_color="#555",
                                      command=self.browse_folder)
        self.btn_browse.pack(pady=(5, 10), padx=30, fill="x")
        
        # Label to show selected path
        self.path_label = ctk.CTkLabel(self.main_frame, text="No drive selected", text_color="#666", font=("Arial", 11))
        self.path_label.pack(pady=(0, 20))

        # 3. Action Button
        self.btn_scan = ctk.CTkButton(self.main_frame, text="💿 START SCAN", 
                                    font=("Arial", 16, "bold"),
                                    height=50, fg_color="#0057e7", hover_color="#004ecb",
                                    state="disabled",
                                    command=self.start_scan)
        self.btn_scan.pack(pady=10, padx=30, fill="x")

        # 4. Results Screen
        self.screen_frame = ctk.CTkTextbox(self.main_frame, height=180, corner_radius=5,
                                         fg_color="black", text_color="#00ff00",
                                         font=("Courier New", 14))
        self.screen_frame.pack(pady=20, padx=30, fill="x")
        self.screen_frame.insert("0.0", "WAITING FOR USB...\n")
        self.screen_frame.configure(state="disabled")

        # 5. SOCIAL BUTTON (New)
        self.btn_insta = ctk.CTkButton(self.main_frame, text="📸 SUPPORT NO-MAD ON INSTAGRAM 🇬🇷",
                                       font=("Arial", 12, "bold"),
                                       fg_color="#C13584", hover_color="#833AB4", # Instagram colors
                                       height=35,
                                       command=self.open_instagram)
        self.btn_insta.pack(pady=(10, 10), padx=30, fill="x")

        # 6. DONATION BUTTON
        self.btn_donation = ctk.CTkButton(self.main_frame, text="☕ BUY ME A COFFEE",
                                          font=("Arial", 12, "bold"),
                                          fg_color="#FF813F", hover_color="#E67E22", # Coffee orange colors
                                          height=35,
                                          command=self.open_donation)
        self.btn_donation.pack(pady=(0, 20), padx=30, fill="x")

    def open_instagram(self):
        webbrowser.open("https://www.instagram.com/no.mad.dj_")

    def open_donation(self):
        webbrowser.open("https://buymeacoffee.com/BaklavaProject")

    def log(self, message):
        self.screen_frame.configure(state="normal")
        self.screen_frame.insert("end", message + "\n")
        self.screen_frame.configure(state="disabled")
        self.screen_frame.see("end")

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        
        if folder_selected:
            self.selected_path = folder_selected
            display_name = os.path.basename(folder_selected)
            if not display_name: display_name = folder_selected
            
            self.path_label.configure(text=f"Selected: {display_name}", text_color="white")
            self.btn_scan.configure(state="normal", fg_color="#0057e7")
            
            self.screen_frame.configure(state="normal")
            self.screen_frame.delete("0.0", "end")
            self.log(f"Ready to scan: {display_name}")
        else:
            self.path_label.configure(text="No drive selected", text_color="#666")

    def start_scan(self):
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def get_fs_type(self, path):
        """Return normalized filesystem token: FAT32, EXFAT, HFS+, APFS or UNKNOWN."""
        try:
            parts = psutil.disk_partitions(all=False)
            best = None
            for p in parts:
                mp = os.path.normpath(p.mountpoint)
                norm_path = os.path.normpath(path)
                if norm_path == mp or norm_path.startswith(mp + os.sep):
                    if best is None or len(mp) > len(best.mountpoint):
                        best = p
            if not best:
                return "UNKNOWN"
            f = (best.fstype or "").lower()
            if "exfat" in f:
                return "EXFAT"
            if "msdos" in f or (f.startswith("fat") and "exfat" not in f):
                return "FAT32"
            if "hfs" in f:
                return "HFS+"
            if "apfs" in f:
                return "APFS"
            return (best.fstype or "UNKNOWN").upper()
        except Exception:
            return "UNKNOWN"

    def run_analysis(self):
        if not self.selected_path:
            self.log("⚠️ Please select a USB drive first")
            return

        profile = PROFILES[self.gear_var.get()]
        fs_type = self.get_fs_type(self.selected_path)

        # Scan files & formats
        flac_count = aiff_count = mp3_count = wav_count = m4a_count = other_count = track_count = 0
        for root, dirs, files in os.walk(self.selected_path):
            if "PIONEER" in root.upper():
                continue
            for file in files:
                f_lower = file.lower()
                if f_lower.endswith(('.mp3', '.wav', '.aiff', '.aif', '.m4a', '.flac')):
                    track_count += 1
                if f_lower.endswith('.flac'):
                    flac_count += 1
                elif f_lower.endswith(('.aiff', '.aif')):
                    aiff_count += 1
                elif f_lower.endswith('.mp3'):
                    mp3_count += 1
                elif f_lower.endswith('.wav'):
                    wav_count += 1
                elif f_lower.endswith('.m4a'):
                    m4a_count += 1
                else:
                    # count other audio-like extensions if needed
                    pass

        # Output header
        self.screen_frame.configure(state="normal")
        self.screen_frame.delete("0.0", "end")
        self.log(f"🔎 ANALYZING: {profile['name']}")
        self.log(f"📍 Drive: {self.selected_path}")
        self.log(f"📊 Filesystem: {fs_type}")
        self.log("-" * 35)

        # Filesystem compatibility
        supported_fs = []
        if profile.get("hfsPlus", False):
            supported_fs.append("HFS+")
        if profile.get("exFat", False):
            supported_fs.append("EXFAT")
        supported_fs.append("FAT32")  # always supported

        if fs_type == "UNKNOWN":
            self.log("⚠️ COULD NOT READ FORMAT (CHECK MANUALLY)")
            fs_ok = False
        elif fs_type in supported_fs:
            self.log("✅ FORMAT COMPATIBLE")
            fs_ok = True
        else:
            self.log("❌ INVALID FORMAT")
            self.log(f"   Detected: {fs_type}")
            self.log(f"   Supported: {', '.join(supported_fs)}")
            fs_ok = False

        # Rekordbox DB
        has_pioneer = any(os.path.exists(os.path.join(self.selected_path, p)) for p in ("PIONEER", ".PIONEER"))
        self.log("✅ REKORDBOX DATABASE FOUND" if has_pioneer else "⚠️ NO 'PIONEER' FOLDER (NO CUES/GRIDS)")

        # Tracks summary
        self.log("📂 AUDIO FILES SUMMARY")
        self.log(f"   🎵 TOTAL TRACKS: {track_count}")
        self.log(f"   • MP3: {mp3_count}")
        self.log(f"   • WAV: {wav_count}")
        self.log(f"   • AIFF: {aiff_count}")
        self.log(f"   • M4A: {m4a_count}")
        self.log(f"   • FLAC: {flac_count}")

        # FLAC support check
        if flac_count > 0:
            if profile.get("noFlac", False):
                self.log(f"❌ {flac_count} FLAC FILES FOUND — {profile['name']} CANNOT PLAY FLAC")
                fs_ok = False
            else:
                self.log(f"✅ {flac_count} FLAC FILES (SUPPORTED)")

        self.log("-" * 35)
        if fs_ok and track_count > 0:
            self.log("🚀 READY FOR GIG")
        elif not fs_ok:
            self.log("🛑 ISSUES DETECTED - CHECK ABOVE")
        else:
            self.log("⚠️ NO AUDIO FILES FOUND")

if __name__ == "__main__":
    app = CDJSimulatorApp()
    app.mainloop()