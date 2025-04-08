import yaml
from box import Box

def load_config():
    """
    Load the configuration from the 'config/config.yaml' file and return it as a Box object.
    """
    with open('config/config.yaml', 'r') as file:
        cfg = Box(yaml.safe_load(file))
    return cfg