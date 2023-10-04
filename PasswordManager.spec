# -*- mode: python ; coding: utf-8 -*-
import os
import sys

# Определяем текущую директорию
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

a = Analysis(
    [os.path.join(current_dir, 'main.py')],
    pathex=[current_dir],
    binaries=[],
    datas=[(os.path.join(current_dir, 'dracula.css'), '.'), (os.path.join(current_dir, 'ico.ico'), '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PasswordManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
