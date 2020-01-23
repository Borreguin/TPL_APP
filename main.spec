# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(50000)

block_cipher = None


a = Analysis(['main.py'],
             pathex=['E:\\proyectos\\TPL_APP', 'E:\\proyectos\\TPL_APP\\gui', 'E:\\proyectos\\TPL_APP\\input',
             'E:\\proyectos\\TPL_APP\\output', 'E:\\proyectos\\TPL_APP\\my_lib'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
