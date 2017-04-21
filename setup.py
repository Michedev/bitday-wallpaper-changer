import os

from setuptools import setup, Command


mainfile = os.path.join(os.path.dirname(__file__), 'src', 'main.py')
name = 'bitday_wallpaper_changer_kde'

class PyInstaller(Command):
    description = "Generate a pyinstaller executable file from main.py"

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
    url='https://github.com/Michedev/bitday-wallpaper-changer',
    author='Michele De Vita',
    author_email='mik3dev@gmail.com',
    description='Python script file that changes automatically the wallpaper of your Linux desktop',
    long_description=read('README.md'),
    license="GPLv3",
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
    ]
)
