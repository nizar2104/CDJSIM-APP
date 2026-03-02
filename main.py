from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineListItem
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import os
import threading
import webbrowser

# Import plyer modules
try:
    from plyer import filechooser
except ImportError:
    filechooser = None


# --- HARDWARE PROFILES ---
PROFILES = {
    # Multi Players
    "CDJ-3000":     {"name": "CDJ-3000",     "noFlac": False, "exFat": True, "hfsPlus": True},
    "CDJ-2000NXS2": {"name": "CDJ-2000NXS2", "noFlac": False, "exFat": False, "hfsPlus": True},
    "CDJ-2000NXS":  {"name": "CDJ-2000NXS",  "noFlac": True,  "exFat": False, "hfsPlus": True},
    "XDJ-1000MK2":  {"name": "XDJ-1000 MK2", "noFlac": False, "exFat": False, "hfsPlus": True},
    "XDJ-1000":     {"name": "XDJ-1000 MK1", "noFlac": True,  "exFat": False, "hfsPlus": True},
    "XDJ-700":      {"name": "XDJ-700",      "noFlac": True,  "exFat": False, "hfsPlus": True},
    
    # All-In-One Systems
    "XDJ-XZ":       {"name": "XDJ-XZ",       "noFlac": False, "exFat": False, "hfsPlus": True},
    "XDJ-RX3":      {"name": "XDJ-RX3",      "noFlac": False, "exFat": True, "hfsPlus": True},
    "XDJ-RR":       {"name": "XDJ-RR",       "noFlac": True,  "exFat": False, "hfsPlus": True},
    "OPUS-QUAD":    {"name": "OPUS-QUAD",    "noFlac": False, "exFat": True, "hfsPlus": True},
    "OMNIS-DUO":    {"name": "OMNIS-DUO",    "noFlac": False, "exFat": True, "hfsPlus": True},
}

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"

        self.selected_path = None
        self.gear_dialog = None

        layout = MDBoxLayout(orientation='vertical', padding="16dp", spacing="16dp")

        title_label = MDLabel(text="CDJ SIMULATOR", halign='center', font_style="H4", theme_text_color="Primary")
        layout.add_widget(title_label)

        author_label = MDLabel(text="BY NO-MAD", halign='center', font_style="Subtitle1", theme_text_color="Secondary")
        layout.add_widget(author_label)

        self.gear_menu_button = MDRaisedButton(text="TARGET: CDJ-3000", on_release=self.show_gear_dialog, pos_hint={'center_x': 0.5})
        layout.add_widget(self.gear_menu_button)
        
        browse_button = MDRaisedButton(text="📂 SELECT DRIVE", on_release=self.browse_folder, pos_hint={'center_x': 0.5})
        layout.add_widget(browse_button)

        self.path_label = MDLabel(text="No drive selected", halign='center', theme_text_color="Secondary")
        layout.add_widget(self.path_label)

        self.scan_button = MDRaisedButton(text="💿 START SCAN", on_release=self.start_scan, md_bg_color=self.theme_cls.primary_color, pos_hint={'center_x': 0.5})
        self.scan_button.disabled = True
        layout.add_widget(self.scan_button)

        self.spinner = MDSpinner(size_hint=(None, None), size=("46dp", "46dp"), pos_hint={'center_x': 0.5})
        layout.add_widget(self.spinner)
        self.spinner.active = False

        scroll = ScrollView(size_hint=(1, 1))
        self.results_label = MDLabel(text="WAITING FOR USB...\n", halign='left', size_hint_y=None, theme_text_color="Primary")
        self.results_label.bind(texture_size=self.results_label.setter('height'))
        scroll.add_widget(self.results_label)
        layout.add_widget(scroll)

        # Social Buttons
        social_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, spacing="16dp", padding=("16dp",0))
        insta_button = MDRaisedButton(text="INSTAGRAM", on_release=self.open_instagram, pos_hint={'center_x': 0.5})
        donation_button = MDRaisedButton(text="BUY ME A COFFEE", on_release=self.open_donation, pos_hint={'center_x': 0.5})
        social_layout.add_widget(insta_button)
        social_layout.add_widget(donation_button)
        layout.add_widget(social_layout)


        return layout

    def show_gear_dialog(self, obj):
        if not self.gear_dialog:
            self.gear_dialog = MDDialog(
                title="Select Target Equipment",
                type="simple",
                items=[OneLineListItem(text=item) for item in PROFILES.keys()],
            )
            self.gear_dialog.items[0].bind(on_release=lambda x: self.set_gear(self.gear_dialog.items[0].text))
            for i in range(1, len(PROFILES.keys())):
                 self.gear_dialog.items[i].bind(on_release=lambda x, item=self.gear_dialog.items[i].text: self.set_gear(item))

        self.gear_dialog.open()
    
    def set_gear(self, gear_text):
        self.gear_menu_button.text = f"TARGET: {gear_text}"
        self.gear_dialog.dismiss()

    def browse_folder(self, *args):
        if not filechooser:
            self.log("Plyer filechooser not available on this platform.")
            return
        if platform == 'android':
             filechooser.choose_dir(on_selection=self.handle_selection)
        else:
             # Fallback for desktop testing
             from tkinter import filedialog
             folder_selected = filedialog.askdirectory()
             if folder_selected:
                self.handle_selection([folder_selected])


    def handle_selection(self, selection):
        if selection:
            self.selected_path = selection[0]
            display_name = os.path.basename(self.selected_path) or self.selected_path
            self.path_label.text = f"Selected: {display_name}"
            self.scan_button.disabled = False
            self.log(f"Ready to scan: {display_name}")
        else:
            self.path_label.text = "No drive selected"

    def start_scan(self, *args):
        self.spinner.active = True
        self.results_label.text = ""
        threading.Thread(target=self.run_analysis, daemon=True).start()

    def log(self, message):
        self.results_label.text += message + "\n"

    def open_instagram(self, *args):
        webbrowser.open("https://www.instagram.com/no.mad.dj_")

    def open_donation(self, *args):
        webbrowser.open("https://buymeacoffee.com/BaklavaProject")

    def run_analysis(self):
        if not self.selected_path:
            self.log("⚠️ Please select a folder first")
            self.spinner.active = False
            return

        gear = self.gear_menu_button.text.replace("TARGET: ", "")
        profile = PROFILES[gear]
        
        self.log(f"🔎 ANALYZING FOR: {profile['name']}\n")
        self.log(f"📍 Drive: {os.path.basename(self.selected_path)}")
        
        # Filesystem check is unreliable on Android, skipping.
        self.log("📊 Filesystem: (SKIPPED ON MOBILE)")
        self.log("-" * 35)

        analysis_ok = True

        # Rekordbox DB
        has_pioneer = any(os.path.exists(os.path.join(self.selected_path, p)) for p in ("PIONEER", ".PIONEER"))
        self.log("✅ REKORDBOX DATABASE FOUND" if has_pioneer else "⚠️ NO 'PIONEER' FOLDER (NO CUES/GRIDS)")

        # Tracks summary
        flac_count = aiff_count = mp3_count = wav_count = m4a_count = track_count = 0
        try:
            for root, dirs, files in os.walk(self.selected_path):
                if "PIONEER" in root.upper():
                    continue
                for file in files:
                    f_lower = file.lower()
                    if f_lower.endswith(('.mp3', '.wav', '.aiff', '.aif', '.m4a', '.flac')):
                        track_count += 1
                    if f_lower.endswith('.flac'): flac_count += 1
                    elif f_lower.endswith(('.aiff', '.aif')): aiff_count += 1
                    elif f_lower.endswith('.mp3'): mp3_count += 1
                    elif f_lower.endswith('.wav'): wav_count += 1
                    elif f_lower.endswith('.m4a'): m4a_count += 1
        except Exception as e:
            self.log(f"ERROR walking directory: {e}")
            self.spinner.active = False
            return

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
                analysis_ok = False
            else:
                self.log(f"✅ {flac_count} FLAC FILES (SUPPORTED)")

        self.log("-" * 35)
        if analysis_ok and track_count > 0:
            self.log("🚀 READY FOR GIG")
        elif not analysis_ok:
            self.log("🛑 ISSUES DETECTED - CHECK ABOVE")
        else:
            self.log("⚠️ NO AUDIO FILES FOUND")

        self.spinner.active = False

if __name__ == "__main__":
    MainApp().run()