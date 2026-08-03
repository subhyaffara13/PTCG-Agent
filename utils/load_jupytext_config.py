import os

def load_jupytext_config(nb_file):
    """Return the jupytext configuration file in the same folder, or in a parent folder, of the current file, if any"""
    config_file = find_jupytext_configuration_file(nb_file)
    if config_file is None:
        return None
    if os.path.isfile(nb_file) and os.path.samefile(config_file, nb_file):
        return None
    config_file = find_jupytext_configuration_file(nb_file)
    return load_jupytext_configuration_file(config_file)

