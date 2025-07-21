# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('click.wav', '.'), 
        ('clicknut.wav', '.'), 
        ('ding.wav', '.'),        # file âm thanh
        ('icon.ico', '.'),         # icon nếu có
               # dữ liệu json
             # nếu có file cấu hình
    ],
    hiddenimports=collect_submodules('modules'),  # nếu import module tự tạo (folder)
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ToolCheckVe',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # ⚠️ True nếu muốn có cửa sổ terminal
    icon='icon.ico'  # icon app nếu có
)
