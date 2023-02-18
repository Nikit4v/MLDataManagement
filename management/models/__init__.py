from pathlib import Path
from .. import configs


def get_default_model_directory():
    return Path(configs.Configuration().get_config()["paths"]["models"])


def get_model_path(name: str, ensure_exists=True) -> Path:
    path = get_default_model_directory() / name
    if ensure_exists:
        if not path.exists():
            raise FileNotFoundError(name)
    return path
