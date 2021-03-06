#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import threading
import subprocess
import json
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
    def __init__(self, preferences, wave_filedir, initial_midi_filepath=''):
        QObject.__init__(self)
        self.preferences = preferences
        self.wave_filedir = wave_filedir
        self.current_wave_filepath = ''
        self.current_midi_filepath = initial_midi_filepath

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

        self.autoPlayOnLoadEnabled = False
        self.loopEnabled = False

    def cleanup(self):
        if os.path.exists(self.wave_filedir):
            shutil.rmtree(self.wave_filedir)

    def filename_changed(self, filename):
        self.setFilenameLabel.emit(filename)

    def media_status_changed(self):
        if self.player.mediaStatus() in [QMediaPlayer.EndOfMedia]:
            if not self.loopEnabled:
                self.player.stop()
                self.isPlaying = False

        elif self.player.mediaStatus() in [QMediaPlayer.StalledMedia]:
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

    def audio_available_changed(self):
        # This method is only used when autoPlayOnLoad is enabled.
        if self.player.isAudioAvailable():
            # QMediaPlayer#play() and pause() effects QMediaPlayer#audioAvailableChanged signal.
            # Thus, we immediately disconnect this method before call play() or pause()
            self.player.audioAvailableChanged.disconnect(self.audio_available_changed)
            self.play_pause_button_clicked()

    def reset_duration_label(self):
        self.setNewEndTimeLabel.emit('--:--')

    def exec_timidity(self, wave_filepath, midi_filepath, on_process_completed=None):
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

        timidity_params_list = [
            [self.preferences['TIMIDITY_LOCATION']],
            config,
            ['-o', wave_filepath, '-Ow', midi_filepath]
        ]
        timidity_params = [item for sublist in timidity_params_list for item in sublist]

        def __exec_timidity():
            proc = subprocess.Popen(
                tuple(timidity_params),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            proc.wait()
            if on_process_completed is not None:
                on_process_completed()
            return

        thread = threading.Thread(target=__exec_timidity)
        thread.start()
        self.toggleBusyIndicator.emit()

    def load_midi_file_immediately(self, midi_filepath):
        self.current_midi_filepath = midi_filepath
        self.should_load_midi_file_immediately()

    """
    Register signals
    """
    loadPreferences = pyqtSignal(str, arguments=['preferencesJson'])
    loadMidiFileImmediately = pyqtSignal(bool, str, arguments=['loadImmediately', 'filePath'])
    setFilenameLabel = pyqtSignal(str, arguments=['newFilenameLabel'])
    toggleBusyIndicator = pyqtSignal()

    setNewCurrentTimeLabel = pyqtSignal(str, arguments=['newCurrentTimeLabel'])
    setNewEndTimeLabel = pyqtSignal(str, arguments=['newEndTimeLabel'])

    setNewCurrentTime = pyqtSignal(int, arguments=['newCurrentTime'])
    setNewEndTime = pyqtSignal(int, arguments=['newEndTime'])

    """
    Register slots
    """
    @pyqtSlot()
    def reflect_preferences(self):
        self.autoPlayOnLoadEnabled = self.preferences['AUTO_PLAY_ON_LOAD_BY_DEFAULT']
        self.loopEnabled = self.preferences['LOOP_BY_DEFAULT']
        # Pass the preferences dictionary to qml as a json string
        self.loadPreferences.emit(
            json.dumps(self.preferences, ensure_ascii=False, indent=4, sort_keys=True, separators=(',', ': '))
        )

    @pyqtSlot()
    def should_load_midi_file_immediately(self):
        self.loadMidiFileImmediately.emit(
            False if self.current_midi_filepath == '' else True,
            self.current_midi_filepath
        )

    @pyqtSlot(str)
    def import_midi_file(self, midi_filepath):
        if midi_filepath == '':
            return

        if self.isPlaying:
            self.player.pause()
            self.isPlaying = False

        self.reset_duration_label()
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

        def __on_process_completed():
            # Track QMediaPlayer#audioAvailableChanged signal when autoPlayOnLoad is enabled
            if self.autoPlayOnLoadEnabled:
                self.player.audioAvailableChanged.connect(self.audio_available_changed)

            self.current_media = QMediaContent(QUrl.fromLocalFile(self.current_wave_filepath))
            self.playlist.addMedia(self.current_media)
            self.playlist.setCurrentIndex(0)
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.toggleBusyIndicator.emit()

        self.exec_timidity(self.current_wave_filepath, self.current_midi_filepath, __on_process_completed)

    @pyqtSlot(str)
    def export_wave_file(self, wave_filepath):
        def __on_process_completed():
            self.toggleBusyIndicator.emit()

        self.exec_timidity(wave_filepath, self.current_midi_filepath, __on_process_completed)

    @pyqtSlot()
    def play_pause_button_clicked(self):
        if self.isPlaying:
            self.player.pause()
        else:
            self.player.play()

        self.isPlaying = not self.isPlaying

    @pyqtSlot(float)
    def set_position(self, position):
        if self.isPlaying:
            self.player.setPosition(int(position))
        else:
            """
            QMediaPlayer sometimes does not automatically buffer the media.
            Thus, we enforce to execute QMediaPlayer::play() to buffer it.
            """
            self.player.play()
            self.player.setPosition(int(position))
            self.player.pause()

    @pyqtSlot(float)
    def set_volume(self, volume):
        self.player.setVolume(int(volume))

    @pyqtSlot()
    def toggle_auto_play_on_load(self):
        self.autoPlayOnLoadEnabled = not self.autoPlayOnLoadEnabled

    @pyqtSlot()
    def toggle_loop(self):
        self.loopEnabled = not self.loopEnabled

    @pyqtSlot(str, str)
    def set_timidity_config(self, config_mode, config_path):
        if self.current_timidity_config_path != config_path:
            self.current_timidity_config_mode = config_mode
            self.current_timidity_config_path = config_path

            # Reload current midi file to reflect the config
            self.import_midi_file(self.current_midi_filepath)
