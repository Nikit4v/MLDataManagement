import copy
from pathlib import Path
from typing import Any, Union
from os import environ

import toml
import platform

CONFIG_PATH = Path("~")
if platform.system() == "Windows":
    CONFIG_PATH = Path(environ["USERPROFILE"] + r"\AppData\Local\MLDataManagement\Configuration.toml")
elif platform.system() == "Linux" or platform.system() == "Darwin":
    CONFIG_PATH = Path(environ["HOME"] + r"/.config/ml_data_management/config.tml")


class Configuration:
    config: dict
    config_path: Path

    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path or CONFIG_PATH)
        self.reload_config()

    def reload_config(self):
        self.config = toml.load(self.config_path)

    def save_config(self):
        toml.dump(self.config, open(self.config_path, "wt"))

    def get_config(self, jsonpath: str = None) -> dict:
        if not isinstance(jsonpath, str) and jsonpath is not None:
            raise ValueError(f"Expected jsonpath to be a string, found {type(jsonpath).__name__}")
        if jsonpath:
            raise NotImplementedError()
        return copy.deepcopy(self.config)

    def update_config(self, *args):
        if len(args) == 1:
            self.config = args[0]
        elif len(args) == 2:
            jsonpath = args[0]
            if not isinstance(jsonpath, str):
                raise ValueError(f"Expected jsonpath to be a string, found {type(jsonpath).__name__}")
            value = args[1]
            raise NotImplementedError()
            # self.__replace_value(self.config, jsonpath, value)

    @classmethod
    def __replace_value(cls, obj: dict | list, jsonpath: str | int, value: Any) -> str | None:
        jsonpath_current_key = jsonpath.split(".", 1)[0]
        jsonpath_next_keys = jsonpath.split(".", 1)[1:]
        if jsonpath_current_key == "":
            raise ValueError("Failed to parse jsonpath key: empty key.")
        if (sub_object := obj.get(jsonpath_current_key) if isinstance(obj, dict) else (
        obj[0] if len(obj) >= 1 else None)) is None:
            return jsonpath_current_key
        is_object = isinstance(sub_object, dict) or isinstance(sub_object, list)
        is_final = len(jsonpath_current_key) == 1
        if is_object and not is_final:
            if isinstance(error_key := cls.__replace_value(sub_object, jsonpath_next_keys, value), str):
                return f"{jsonpath_current_key}.{error_key}"
