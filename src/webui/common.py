import os

elements = {}
web_log_dir = "logs"
data_dir = "data"
css_dir = 'src/webui/css'
device = "cuda"

settings = {
    "base_model": None,
    "path_to_model": {}
}

def get_save_dir():
    if not settings["base_model"]:
        return None
    return os.path.join(web_log_dir, settings["base_model"])

def set_base_model(model_name):
    settings["base_model"] = model_name

def add_base_model(model_name, model_path):
    settings["path_to_model"][model_name] = model_path

def del_base_model(model_name):
    settings["path_to_model"].pop(model_name)
