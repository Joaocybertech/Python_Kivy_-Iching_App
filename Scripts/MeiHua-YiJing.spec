# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['kivyapp_teste.py'],
             pathex=['C:/Users/joaot/Desktop/Meus tesouros/xubsdevs/novoflor'],
             binaries=[],
             datas=[('meu_icone.ico', '.'),  # substituído .png por .ico
                    ('dicionario_hexagrama.py', '.'), 
                    ('Meihua.py', '.'), 
                    ('métodos_de_pergunta.py', '.'), 
                    ('saved_questions.json', '.'), 
                    ('savefilecopy.py', '.'),
                    ('Roboto-Medium.ttf', '.')],
             hiddenimports=['kivy', 'kivymd', 'datetime', 'json', 'webbrowser', 'kivy.core.text', 'os'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Meihua-Yijing',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True,
          icon='meu_icone.ico' )  # here is the icon setting
