PyQTimidity
===========

A small macOS GUI of timidity++ for playing midi files.

timidity++ を使って MIDI ファイルを再生するための macOS 用 GUI.

Usage
-----

*  先に timidity++ をインストールしておいてください.
    -  [Homebrew](https://brew.sh/index_ja.html) を使えば、`brew install timidity` で完了します.
    
*  後は、PyQTimidity を起動して MIDI ファイルを読み込めば OK です.
    -  PyQTimidity は標準で `/usr/local/bin/timidity` を読み込もうとします. これを変更する場合には、PyQTimidity の初回起動時に生成される `~/.py-qtimidity-pref.json` の `"TIMIDITY_LOCATION"` の値を書き換えてください.

Development
-----------

*  Python version
    -  3.5.2
*  Qt5 version
    -  5.9.2
*  PyQt5 version
    -  5.9.1
*  PyInstaller version
    -  3.3

License
-------

*  GPL 3.0
