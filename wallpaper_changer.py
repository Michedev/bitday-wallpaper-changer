import os

import datetime

import time

import sys

from os.path import join as join_paths

import subprocess

def get_resolution():
    if len(sys.argv) == 1:
        if os.path.exists(opt_cfg_file):
            with open(opt_cfg_file) as f:
                return f.read()
        else:
            return subprocess.run("xrandr  | grep \* | cut -d' ' -f4", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8').replace('\n', '')
    elif len(sys.argv) == 2:
        return sys.argv[2]
    else:
        message = "Accepted input are:\n- No input: read from %s or get your desktop resolution\n- One argument input:  is your resolution"
        raise ValueError(message)


def change_wallpaper_command(path_img: str) -> str:
    path_img = path_img if path_img.startswith('file:///') else 'file://' + path_img
    script = 'string: var Desktops = desktops();' \
             'for (i=0;i<Desktops.length;i++)' \
             ' {' \
             'd = Desktops[i]; ' \
             'd.wallpaperPlugin = "org.kde.image";' \
             '  d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");' \
             ' d.writeConfig("Image", "%s"); ' \
             '}' % path_img
    command = "qdbus org.kde.plasmashell /PlasmaShell evaluateScript '%s'" % script
    return command


def is_even(num):
    return num % 2 == 0


def get_img_path_by_hour(hour: int) -> str:
    hour = hour if is_even(hour) else hour - 1
    index_img = pair_hour_to_index[hour]
    return img_paths[index_img]


def seconds_to_next_img(time: {'hour', 'minute', 'second'}) -> int:
    remaining_hours = 1 if is_even(time.hour) else 0
    remaining_minutes = 60 - time.minute
    remaining_seconds = remaining_minutes * 60 + remaining_hours * 3600 - time.second
    return remaining_seconds


def change_wallpaper():
    time_now = datetime.datetime.now()
    img_path = get_img_path_by_hour(time_now.hour)
    cmd = change_wallpaper_command(img_path)
    code = os.system(cmd)
    if code == 512: #widged locked
        sys.exit(1)

ten_minutes = 600 #seconds

opt_cfg_file = join_paths(os.environ['HOME'], '.config', 'wallpaper_changer_res.cfg')

resolution = get_resolution()
path_images = os.environ['HOME'] + '/Pictures/BitDay-2-%s/%s/' % (resolution, resolution)
img_paths = [join_paths(path_images, img) for img in os.listdir(path_images)]

pair_hour_to_index = dict([(hour, index) for index, hour in enumerate(range(6, 22 + 1, 2))])
pair_hour_to_index.update({0: 9, 2: 10, 4: 11})

change_wallpaper()
while True:
    wait_time = min(ten_minutes, seconds_to_next_img(datetime.datetime.now()))
    time.sleep(wait_time)
    change_wallpaper()
