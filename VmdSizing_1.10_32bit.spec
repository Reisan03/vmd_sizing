# -*- mode: python -*-

block_cipher = None


a = Analysis(['src\\wrapper.py'],
             pathex=['c:\\MMD\\vmd_sizing'],
             binaries=[],
             datas=[],
             hiddenimports=['wx._adv', 'wx._html'],
             hookspath=[],
             runtime_hooks=[],
             excludes=['mkl','libopenblas'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='VmdSizing_1.10_32bit',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )