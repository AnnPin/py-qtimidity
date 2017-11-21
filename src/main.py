#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import json
import tempfile
import subprocess
import random
import string
import shutil
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist

# Do this import for the pyinstaller PyQt.Quick hook.
from PyQt5 import QtQuick

PREFERENCES_FILE_PATH = os.path.expanduser(os.path.join('~', '.py-qtimidity-pref.json'))
MAIN_QML = 'qml/main.qml'
PREFERENCES_ERROR_QML = 'qml/preferences_error.qml'


def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInsteller
    https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    try:
        # PyInstaller creates a temp foldter and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


def get_default_preferences():
    default_pref = {
        "TIMIDITY_LOCATION": "/usr/local/bin/timidity"
    }
    return default_pref


def generate_random_string(length):
    chars = string.digits + string.ascii_letters
    rand = random.SystemRandom()
    return ''.join([rand.choice(chars) for _ in range(length)])


class Timidity(QObject):
    def __init__(self, preferences, wave_filedir):
        QObject.__init__(self)
        self.preferences = preferences
        self.wave_filedir = wave_filedir
        self.current_wave_filepath = ''
        self.current_midi_filepath = ''

        self.current_media = None
        self.playlist = QMediaPlaylist()
        self.player = QMediaPlayer()
        self.player.setPlaylist(self.playlist)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.isPlaying = False
        self.isMediaLoaded = False
        self.loopEnabled = False

    def cleanup(self):
        if os.path.exists(self.wave_filedir):
            shutil.rmtree(self.wave_filedir)

    def filename_changed(self, filename):
        self.setFilenameLabel.emit(filename)

    def media_status_changed(self):
        if self.player.mediaStatus() in [QMediaPlayer.LoadedMedia, QMediaPlayer.BufferedMedia]:
            self.isMediaLoaded = True

        elif self.player.mediaStatus() in [QMediaPlayer.NoMedia, QMediaPlayer.LoadingMedia]:
            self.isMediaLoaded = False

        elif self.player.mediaStatus() in [QMediaPlayer.EndOfMedia]:
            if not self.loopEnabled:
                self.player.stop()
                self.isPlaying = False

    def position_changed(self):
        position_milliseconds = self.player.position()
        self.setNewCurrentTime.emit(position_milliseconds)

        position_seconds = int(position_milliseconds / 1000)
        self.setNewCurrentTimeLabel.emit(
            '{}:{:02d}'.format(position_seconds // 60, position_seconds % 60)
        )

    def duration_changed(self):
        duration_milliseconds = self.player.duration()
        self.setNewEndTime.emit(duration_milliseconds)

        duration_seconds = int(duration_milliseconds / 1000)
        self.setNewEndTimeLabel.emit(
            '{}:{:02d}'.format(duration_seconds // 60, duration_seconds % 60)
        )

    def exec_timidity(self, wave_filepath, midi_filepath):
        subprocess.run(
            (self.preferences['TIMIDITY_LOCATION'], '-o', wave_filepath, '-Ow', midi_filepath),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    """
    Register signals
    """
    setFilenameLabel = pyqtSignal(str, arguments=['newFilenameLabel'])
    setLoopLabel = pyqtSignal(str, arguments=['newLoopLabel'])

    setNewCurrentTimeLabel = pyqtSignal(str, arguments=['newCurrentTimeLabel'])
    setNewEndTimeLabel = pyqtSignal(str, arguments=['newEndTimeLabel'])

    setNewCurrentTime = pyqtSignal(int, arguments=['newCurrentTime'])
    setNewEndTime = pyqtSignal(int, arguments=['newEndTime'])

    """
    Register slots
    """
    @pyqtSlot(str)
    def inport_midi_file(self, filepath):
        if self.isPlaying:
            self.player.pause()
            self.isPlaying = False

        self.playlist.clear()
        if self.current_wave_filepath is not '':
            os.remove(self.current_wave_filepath)

        self.current_midi_filepath = re.sub('^file://', '', filepath)
        orig_filename = self.current_midi_filepath.split(os.sep)[-1]
        self.filename_changed(orig_filename)

        wave_filename = '{}-{}.wav'.format(
            orig_filename,
            generate_random_string(8)
        )
        self.current_wave_filepath = os.path.join(self.wave_filedir, wave_filename)
        self.exec_timidity(self.current_wave_filepath, self.current_midi_filepath)

        self.current_media = QMediaContent(QUrl.fromLocalFile(self.current_wave_filepath))
        self.playlist.addMedia(self.current_media)
        self.playlist.setCurrentIndex(0)
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

    @pyqtSlot(str)
    def export_wave_file(self, filepath):
        wave_filepath = re.sub('^file://', '', filepath)
        self.exec_timidity(wave_filepath, self.current_midi_filepath)

    @pyqtSlot()
    def play_pause_button_clicked(self):
        if not self.isMediaLoaded:
            return

        if self.isPlaying:
            self.player.pause()
        else:
            self.player.play()

        self.isPlaying = not self.isPlaying

    @pyqtSlot(float)
    def set_position(self, position):
        if not self.isMediaLoaded:
            return

        if self.isPlaying:
            self.player.setPosition(int(position))
        else:
            self.player.play()
            self.player.setPosition(int(position))
            self.player.pause()

    @pyqtSlot(float)
    def set_volume(self, volume):
        self.player.setVolume(int(volume))

    @pyqtSlot()
    def toggle_loop(self):
        self.loopEnabled = not self.loopEnabled
        self.setLoopLabel.emit(
            "Disable loop" if self.loopEnabled else "Enable loop"
        )


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    timidity = None

    if not os.path.exists(PREFERENCES_FILE_PATH):
        pref_dict = get_default_preferences()
        with open(PREFERENCES_FILE_PATH, 'w') as f:
            f.write(json.dumps(pref_dict))

    with open(PREFERENCES_FILE_PATH) as f:
        try:
            preferences = json.load(f)
            wave_filedir = tempfile.mkdtemp('-tmp', 'py-qtimidity-')
            timidity = Timidity(preferences, wave_filedir)
            qml_path = resource_path(MAIN_QML)
            engine.rootContext().setContextProperty('timidity', timidity)

        except ValueError:
            qml_path = resource_path(PREFERENCES_ERROR_QML)

    url = QUrl(
        os.path.join(
            os.path.dirname(__file__), qml_path
        )
    )

    engine.load(url)
    rc = app.exec_()

    if timidity is not None:
        timidity.cleanup()

    del engine
    del app
    sys.exit(rc)

if __name__ == '__main__':
    main()

