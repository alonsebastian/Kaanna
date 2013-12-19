#!/usr/bin/python
# -*- coding: UTF-8 -*-

try:
    from setuptools import setup, find_packages, Extension
except ImportError:
    import ez_setup
    ez_setup.use_setuptools()
    from setuptools import setup, find_packages, Extension

import os
import platform

python_version = platform.python_version()[0:3]

setup_info = dict(name = 'Kaanna',
        version = '1.0',
        description = 'Everyday translator',
        author = 'Sebastian Alonso',
        author_email = 'alon.sebastian@gmail.com',
        long_description = """Kaanna is a small translator that allows you to translate between 87 different languages, based on the google translate API. Thought to make your everyday translation easier, Kaanna includes a lot of features specially design to be intuitive and easy-to-use. One of our goals is to be multi-platform in order to get to a wider range of users.""",
        url = 'http://kaanna.com.ar',
        license = 'GNU GPL 3',
        ext_package = "Kaanna",)

def windows_check():
    return platform.system() in ('Windows', 'Microsoft')

def osx_check():
    return platform.system() == "Darwin"


if os.name == 'nt':
    import py2exe

    _data_files = ['dlls/Microsoft.VC90.CRT.manifest',
            'dlls/msvcm90.dll',
            'dlls/msvcp90.dll',
            'dlls/msvcr71.dll',
            'dlls/msvcr90.dll',
            'conf/default.cfg',
            'conf/conf.cfg',]


    opts = {
        'py2exe': {
            'packages': ['encodings', 'gtk', 'codecs'],
            'includes': ['locale', 'cairo', 'pangocairo', 'pango',
                'atk', 'gobject', 'os', 'code', 'win32api', 'win32clipboard',
                'win32gui', 'win32con', 'pyHook', 'gtkwin32', 'conf', 'translation',
                'urllib2', 'urllib', 'ConfigParser'],
            'excludes': ['ltihooks', 'pywin', 'pywin.debugger',
                'pywin.debugger.dbgcon', 'pywin.dialogs',
                'pywin.dialogs.list', 'Tkconstants', 'Tkinter', 'tcl'
                'doctest', 'macpath', 'pdb', 'cookielib', 'ftplib',
                'pickle', 'caledar', 'win32wnet',
                'getopt', 'gdk', 'email'],
            'dll_excludes': ['libglade-2.0-0.dll', 'w9xpopen.exe'],
            'optimize': '2',
            'dist_dir': '../dist',
            "skip_archive": 1
        }
    }

    setup(requires    = ["gtk"],
        windows        = [{"script": "Translator.py", 'icon_resources': [(1, "Resources\kaanna.ico")]}],
        options        = opts,
        data_files    = _data_files, **setup_info)

    print "done! files at: dist"