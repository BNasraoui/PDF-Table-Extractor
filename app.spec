# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Create runtime hook to fix Tkinter menu bar crash on macOS
with open('tk_fix.py', 'w') as f:
    f.write('import os\nos.environ["_PYTHON_HOST_COMPLETE"] = "disable-tk-menu"\n')

a = Analysis(
    ['pdf_table_extractor.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PIL', 'PIL._imagingtk', 'PIL._tkinter_finder', 'pdfplumber.utils'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['tk_fix.py'],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Add customtkinter files - fixed approach
import os
import sys
import site
import customtkinter
from pathlib import Path

# Find customtkinter path
ctk_path = Path(customtkinter.__file__).parent

# Add each file individually
for root, dirs, files in os.walk(str(ctk_path)):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, str(ctk_path))
        dest_path = os.path.join('customtkinter', rel_path)
        a.datas.append((dest_path, full_path, 'DATA'))

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PDF Table Extractor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PDF Table Extractor',
)

app = BUNDLE(
    coll,
    name='PDF Table Extractor.app',
    icon=None,
    bundle_identifier='com.example.pdftableextractor',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'NSHighResolutionCapable': 'True',
        'NSRequiresAquaSystemAppearance': 'False',  # For dark mode support
    }
) 