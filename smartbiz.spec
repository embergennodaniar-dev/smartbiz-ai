# -*- mode: python ; coding: utf-8 -*-
# SmartBiz AI — PyInstaller spec
# Ishlatish: pyinstaller smartbiz.spec

import os
block_cipher = None

BASE = os.path.abspath('.')
BACKEND = os.path.join(BASE, 'backend')
FRONTEND = os.path.join(BASE, 'frontend')

a = Analysis(
    [os.path.join(BASE, 'launcher.py')],
    pathex=[BASE, BACKEND],
    binaries=[],
    datas=[
        # Backend Python fayllari
        (os.path.join(BACKEND, 'main.py'),              'backend'),
        (os.path.join(BACKEND, 'routers'),              'backend/routers'),
        (os.path.join(BACKEND, 'models'),               'backend/models'),
        (os.path.join(BACKEND, 'lang'),                 'backend/lang'),
        (os.path.join(BACKEND, 'demo'),                 'backend/demo'),
        # Frontend
        (os.path.join(FRONTEND, 'templates'),           'frontend/templates'),
        (os.path.join(FRONTEND, 'static'),              'frontend/static'),
    ],
    hiddenimports=[
        # FastAPI / Uvicorn
        'uvicorn', 'uvicorn.main', 'uvicorn.config', 'uvicorn.server',
        'uvicorn.lifespan.on', 'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.auto', 'uvicorn.loops.auto',
        'fastapi', 'fastapi.middleware.cors', 'fastapi.staticfiles',
        'starlette', 'starlette.routing', 'starlette.middleware',
        'starlette.staticfiles', 'starlette.responses',
        # SQLAlchemy
        'sqlalchemy', 'sqlalchemy.dialects.sqlite',
        'sqlalchemy.orm', 'sqlalchemy.ext.declarative',
        # Auth
        'jose', 'jose.jwt', 'passlib', 'passlib.context',
        'passlib.handlers.bcrypt', 'bcrypt',
        # Pydantic
        'pydantic', 'pydantic.v1',
        # Multipart
        'multipart', 'python_multipart',
        # Gemini (optional)
        'google.generativeai',
        # Stdlib
        'email.mime.text', 'email.mime.multipart',
        'csv', 'io', 'json', 'os', 'sys', 'threading',
        'datetime', 'typing', 'random', 'math',
        # Tkinter (launcher GUI)
        'tkinter', 'tkinter.ttk', 'tkinter.messagebox',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'PIL', 'cv2', 'torch'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SmartBizAI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,        # GUI rejim — qora terminal ko'rinmasin
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon='icon.ico',   # Icon qo'shmoqchi bo'lsangiz — shu yerga
)
