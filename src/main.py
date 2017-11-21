#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import tempfile
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from app_core import AppCore

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


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)

    app_core = None

    if not os.path.exists(PREFERENCES_FILE_PATH):
        pref_dict = get_default_preferences()
        with open(PREFERENCES_FILE_PATH, 'w') as f:
            f.write(json.dumps(pref_dict))

    with open(PREFERENCES_FILE_PATH) as f:
        try:
            preferences = json.load(f)
            wave_filedir = tempfile.mkdtemp('-tmp', 'py-qtimidity-')
            app_core = AppCore(preferences, wave_filedir)
            qml_path = resource_path(MAIN_QML)
            engine.rootContext().setContextProperty('app_core', app_core)

        except ValueError:
            qml_path = resource_path(PREFERENCES_ERROR_QML)

    url = QUrl(
        os.path.join(
            os.path.dirname(__file__), qml_path
        )
    )

    engine.load(url)
    rc = app.exec_()

    if app_core is not None:
        app_core.cleanup()

    del engine
    del app
    sys.exit(rc)

if __name__ == '__main__':
    main()

