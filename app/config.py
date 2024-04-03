import json
import os


def get_config():
    module_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(module_dir, "config.json")
    try:
        with open(config_file_path, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        raise FileNotFoundError("Config file not found.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Error decoding config file: {e}")


def get_security_config():
    try:
        return get_config()["security"]
    except KeyError:
        raise RuntimeError("Config file has not security configuration")
    except Exception as exception:
        raise RuntimeError(f"Error reading config: {exception}") from exception


def get_users_config():
    try:
        return get_config()["users"]
    except KeyError:
        raise RuntimeError("Config file has not users configuration")
    except Exception as exception:
        raise RuntimeError(f"Error reading config: {exception}") from exception
