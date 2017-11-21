default:
	pyinstaller main.spec

spec:
	pyinstaller src/main.py --onefile --noconsole --windowed
