
import unittest
from unittest.mock import MagicMock, patch
from main import MainApp, PROFILES

class TestAppAnalysis(unittest.TestCase):
    def setUp(self):
        self.app = MainApp()
        self.app.results_label = MagicMock()
        self.app.log = self.app.results_label.text

    @patch('os.walk')
    def test_analysis_with_flac_on_cdj3000(self, mock_walk):
        # CDJ-3000 supports FLAC
        self.app.gear_menu_button = MagicMock()
        self.app.gear_menu_button.text = "TARGET: CDJ-3000"
        self.app.selected_path = "/fake/drive"
        
        mock_walk.return_value = [
            ('/fake/drive', [], ['track1.mp3', 'track2.flac']),
        ]
        
        self.app.run_analysis()
        
        # Check that no error is logged for FLAC
        log_text = self.app.log.__iadd__.call_args.args[0]
        self.assertNotIn("CANNOT PLAY FLAC", log_text)

    @patch('os.walk')
    def test_analysis_with_flac_on_cdj2000nxs(self, mock_walk):
        # CDJ-2000NXS does NOT support FLAC
        self.app.gear_menu_button = MagicMock()
        self.app.gear_menu_button.text = "TARGET: CDJ-2000NXS"
        self.app.selected_path = "/fake/drive"

        mock_walk.return_value = [
            ('/fake/drive', [], ['track1.mp3', 'track2.flac']),
        ]
        
        self.app.run_analysis()
        
        # Check that an error is logged for FLAC
        log_text = self.app.log.__iadd__.call_args.args[0]
        self.assertIn("CANNOT PLAY FLAC", log_text)

    @patch('os.walk')
    def test_no_audio_files_found(self, mock_walk):
        self.app.gear_menu_button = MagicMock()
        self.app.gear_menu_button.text = "TARGET: CDJ-3000"
        self.app.selected_path = "/fake/drive"
        
        mock_walk.return_value = [
            ('/fake/drive', [], ['document.txt', 'archive.zip']),
        ]
        
        self.app.run_analysis()
        
        log_text = self.app.log.__iadd__.call_args.args[0]
        self.assertIn("NO AUDIO FILES FOUND", log_text)

if __name__ == '__main__':
    unittest.main()
