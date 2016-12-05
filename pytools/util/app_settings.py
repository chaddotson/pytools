from sys import platform
from os import environ
from os.path import exists, expanduser, join
from os import makedirs


def ensure_app_settings_directory(appname):
    if platform == 'win32':
        appdata_path = join(environ['APPDATA'], appname)

    else:
        appdata_path = expanduser(join("~", "." + appname))

    if not exists(appdata_path):
        makedirs(appdata_path)

    return appdata_path