from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        layout = MDBoxLayout(orientation='vertical', padding=50, spacing=20)
        label = MDLabel(text="CDJ Simulator", halign='center', theme_text_color="Primary")
        layout.add_widget(label)
        layout.add_widget(MDRaisedButton(text="Analyze USB Drive", on_release=self.analyze_usb, pos_hint={'center_x': 0.5}))
        return layout

    def analyze_usb(self, *args):
        print("Analyze USB button pressed")


if __name__ == "__main__":
    MainApp().run()
