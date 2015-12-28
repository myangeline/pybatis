import os

from core.error import ConfigException
from utils.fileutil import read_file


def load_config(config_path):
    if not config_path:
        raise ConfigException("配置文件路径不可以为空")
    if not os.path.exists(config_path):
        raise ConfigException("配置文件路径不存在")

    config_content = read_file(config_path)
