# LocalMediaServer.spec
# Build with:  pyinstaller --clean --noconfirm LocalMediaServer.spec

import os
from PyInstaller.utils.hooks import collect_all
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

# Project root (where this spec file is and where app/ is)
project_dir = os.path.abspath(os.getcwd())

# Collect package data/hidden imports automatically for these libs
packages_to_collect = [
    "fastapi",
    "starlette",
    "pydantic",
    "pydantic_core",
    "sqlmodel",
    "anyio",
    "typing_extensions",
]

hiddenimports = []
datas = []
binaries = []

for pkg in packages_to_collect:
    c_datas, c_binaries, c_hidden = collect_all(pkg)
    datas += c_datas
    binaries += c_binaries
    hiddenimports += c_hidden

# Add your app files (static and API routers, plus modules)
datas += [
    (os.path.join(project_dir, "app", "static"), "app/static"),
    (os.path.join(project_dir, "app", "routers"), "app/routers"),
    (os.path.join(project_dir, "app", "__init__.py"), "app"),
    (os.path.join(project_dir, "app", "db.py"), "app"),
    (os.path.join(project_dir, "app", "scanner.py"), "app"),
    (os.path.join(project_dir, "app", "settings.py"), "app"),
]

a = Analysis(
    ['server_entry.py'],  # entrypoint
    pathex=[project_dir],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='LocalMediaServer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,         # safer; set True only if you have UPX installed
    console=True,      # True = keep console for logs; False = hide
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    name='LocalMediaServer',
    strip=False,
    upx=False,
    upx_exclude=[],
)
