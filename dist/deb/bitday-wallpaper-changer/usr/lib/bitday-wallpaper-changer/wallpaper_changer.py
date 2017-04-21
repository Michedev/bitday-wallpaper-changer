import datetime
import os
import subprocess
import sys
from os.path import join as join_paths

github_repo = "https://github.com/Michedev/bitday-wallpaper-changer"

def get_resolution(cfg_file=None):
    if len(sys.argv) == 1:
        if cfg_file and os.path.exists(cfg_file):
            with open(cfg_file) as f:
                return f.read()
        else:
            return subprocess.run("xrandr  | grep \* | cut -d' ' -f4", stdout=subprocess.PIPE,
                                  shell=True).stdout.decode('utf-8').replace('\n', '')
    elif len(sys.argv) == 2:
        return sys.argv[1]
    else:
        message = "Accepted input are:\n" + \
                 ("- No input: read from %s or get your desktop resolution\n" % "xrandr  | grep \* | cut -d' ' -f4") + \
                  "- One argument input:  is your resolution"
        raise ValueError(message)


def change_wallpaper_command(path_img: str) -> str:
    path_img = path_img if path_img.startswith('file:///') else 'file://' + path_img
    DE = os.environ['XDG_CURRENT_DESKTOP'].upper()
    if 'KDE' in DE:
        return change_wallpaper_command_kde(path_img)
    elif any([de in DE for de in ['UNITY', 'MATE', 'XFCE', 'GNOME', 'BUDGIE']]):
        return change_wallpaper_command_gnome(path_img)
    else:
        print('Desktop enviroment not found from enviroment variable XDG_CURRENT_DESKTOP (Current UPPER value %s),'
              ' please report this issue in %s' % (DE, github_repo))
        sys.exit(1)


def change_wallpaper_command_gnome(path_img: str) -> str:
    command = "gsettings set org.gnome.desktop.background picture-uri " + path_img
    return command


def change_wallpaper_command_kde(path_img: str) -> str:
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
    index_img = hour_to_index[hour]
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
    if code == 512:  # widged locked
        sys.exit(1)


opt_cfg_file = join_paths(os.environ['HOME'], '.config', 'wallpaper_changer_res.cfg')

resolution = get_resolution(opt_cfg_file)
path_images = os.environ['HOME'] + '/Pictures/BitDay-2-%s/%s/' % (resolution, resolution)
try:
    img_paths = [join_paths(path_images, img) for img in os.listdir(path_images)]
except FileNotFoundError:
    print(
        "Path not exist: %s\n"
        "Please go to %s for more info about this software execution" % (path_images, github_repo))
    sys.exit(1)
hour_to_index = dict([(hour, index) for index, hour in enumerate(range(6, 22 + 1, 2))])
hour_to_index.update({0: 9, 2: 10, 4: 11})
