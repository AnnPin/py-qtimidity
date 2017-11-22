# -*- mode: python -*-

block_cipher = None


a = Analysis(['src/main.py'],
             pathex=['/Users/Luna/src/github.com/AnnPin/py-qtimidity'],
             binaries=[],
             datas=[
                 ('src/qml', 'qml')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyQTimidity',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyQTimidity')
app = BUNDLE(coll,
             name='PyQTimidity.app',
             info_plist={'NSHighResolutionCapable': 'True'},
             icon="icon.icns",
             bundle_identifier='com.annpin.PyQTimidity')
