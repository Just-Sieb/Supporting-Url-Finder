# -*- mode: python -*-

block_cipher = None


added_files = [('url.ico', '.')]

a = Analysis(['gui.py'],
             pathex=['C:\\Users\\Justin.Siebert\\Code\\Supporting-Url-Finder'],
             binaries=None,
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += [('url.ico','C:\\Users\Justin.Siebert\\Code\\Supporting-Url-Finder\\url.ico','DATA')]

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gui',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='url.ico')
