default:
	rm -f src/qml/*.qmlc
	pyinstaller main.spec
	cp -f config/Info.plist dist/PyQTimidity.app/Contents/Info.plist

spec:
	pyinstaller src/main.py --noconsole --windowed
