# -*- utf-8 -*-

import configparser
from .import FileUtils

cf = configparser.ConfigParser()
cf.read(FileUtils.joinPath("..", "conf", "pixiv"))