import music21
import os
import platform

class MidiScore:
    def __init__(self):
        return

    @classmethod
    def music21_env(cls):
        us = music21.environment.UserSettings()
        # Path to music21 environment
        us_path = us.getSettingsPath()
        if not os.path.exists(us_path):
            us.create()

        if platform == "Windows":
            # for windows
            us['musescoreDirectPNGPath'] = r'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe' 
            us['musicxmlPath'] = r'C:\\Program Files\\MuseScore 3\\bin\\MuseScore3.exe'

        elif platform == "Linux":
            us['musescoreDirectPNGPath'] = '/usr/bin/mscore'
            us['musicxmlPath'] = '/usr/bin/mscore'

    @classmethod
    def build_score(cls, midi_filename):
        cls.music21_env()
        score = music21.converter.parse(midi_filename)
        return score

    @classmethod
    def show_score(cls, midi_filename):
        score = cls.build_score(midi_filename)
        score.show()

    @classmethod
    def score_pdf_xml(cls, midi_filename, filename="score", dest_path="../"):
        score = cls.build_score(midi_filename)
        score.write(filename + ".pdf", fp=dest_path)