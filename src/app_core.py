#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import shutil
import random
import string
from PyQt5.QtCore import QUrl, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist


def generate_random_string(length):
    chars = string.digits + string.ascii_letters
    rand = random.SystemRandom()
    return ''.join([rand.choice(chars) for _ in range(length)])


class AppCore(QObject):
    def __init__(self, preferences, wave_filedir):
        QObject.__init__(self)
        self.preferences = preferences
        self.wave_filedir = wave_filedir
        self.current_wave_filepath = ''
        self.current_midi_filepath = ''

        self.current_timidity_config_mode = 'default'
        self.current_timidity_config_path = ''

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
        config_mode = self.current_timidity_config_mode
        config_path = self.current_timidity_config_path
        config = None

        if config_mode == 'sf':
            cfg_filepath = os.path.join(self.wave_filedir, "soundfont.cfg")
            with open(cfg_filepath, 'w') as f:
                f.write('soundfont "{}"'.format(config_path))
            config = ['-c', cfg_filepath]
        elif config_mode == 'cfg':
            config = ['-c', config_path]
        elif config_mode == 'default':
            config = []

        """
        timidity -c /usr/local/Cellar/timidity/2.14.0/share/msgs/msgs.cfg ~/Downloads/nm/nm35.mid
        """

        timidity_params_list = [
            [self.preferences['TIMIDITY_LOCATION']],
            config,
            ['-o', wave_filepath, '-Ow', midi_filepath]
        ]
        timidity_params = [item for sublist in timidity_params_list for item in sublist]
        subprocess.run(
            tuple(timidity_params),
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
    def import_midi_file(self, midi_filepath):
        if midi_filepath == '':
            return

        if self.isPlaying:
            self.player.pause()
            self.isPlaying = False

        self.playlist.clear()
        if self.current_wave_filepath is not '':
            os.remove(self.current_wave_filepath)

        self.current_midi_filepath = midi_filepath
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
    def export_wave_file(self, wave_filepath):
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
            'Disable loop' if self.loopEnabled else 'Enable loop'
        )

    @pyqtSlot(str, str)
    def set_timidity_config(self, config_mode, config_path):
        if self.current_timidity_config_path != config_path:
            self.current_timidity_config_mode = config_mode
            self.current_timidity_config_path = config_path

            # Reload current midi file to reflect the config
            self.import_midi_file(self.current_midi_filepath)
