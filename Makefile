default:
	pyinstaller main.spec
	cp -f config/Info.plist dist/PyQTimidity.app/Contents/Info.plist

spec:
	pyinstaller src/main.py --onefile --noconsole --windowed
