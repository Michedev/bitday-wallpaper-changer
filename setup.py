import os

from setuptools import setup, Command

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

mainfile = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
name = 'bitday_wallpaper_changer_kde'

class PyInstaller(Command):
    description = "Generate a pyinstaller executable file"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('pyinstaller -F -n %s %s' % (name, mainfile))


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=name,
    version='1.0.0',
    py_modules=['src.wallpaper_changer', 'src.main'],
    url='https://github.com/Michedev/bitday-wallpaper-changer-kde',
    author='Michele De Vita',
    author_email='mik3dev@gmail.com',
    options={"build_exe": build_exe_options},
    description='Python script file that changes automatically the wallpaper of your KDE desktop',
    long_description=read('README.md'),
    python_requires='>=3.5',
    entry_points={
        'console_scripts': ['bitday_wallpaper_changer=src.main:main']
    },
    cmdclass={
        'pyinstaller': PyInstaller
    },
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment :: K Desktop Environment (KDE)'
    ]
)
