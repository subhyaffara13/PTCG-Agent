
def global_jupytext_configuration_directories():
    """Return the directories in which Jupytext will search for a configuration file"""

    config_dirs = []

    if "XDG_CONFIG_HOME" in os.environ:
        config_dirs.extend(os.environ["XDG_CONFIG_HOME"].split(":"))
    elif "USERPROFILE" in os.environ:
        config_dirs.append(os.environ["USERPROFILE"])
    elif "HOME" in os.environ:
        config_dirs.append(os.path.join(os.environ["HOME"], ".config"))
        config_dirs.append(os.environ["HOME"])

    if "XDG_CONFIG_DIRS" in os.environ:
        config_dirs.extend(os.environ["XDG_CONFIG_DIRS"].split(":"))
    elif "ALLUSERSPROFILE" in os.environ:
        config_dirs.append(os.environ["ALLUSERSPROFILE"])
    else:
        config_dirs.extend(["/usr/local/share/", "/usr/share/"])

    for config_dir in config_dirs:
        yield from [
            os.path.join(config_dir, "jupytext"),
            config_dir,
        ]

