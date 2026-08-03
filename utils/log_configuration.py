import os
import sys

def log_configuration(manager: BuildManager, sources: list[BuildSource]) -> None:
    """Output useful configuration information to LOG and TRACE"""

    if not manager.logging_enabled:
        return

    config_file = manager.options.config_file
    if config_file:
        config_file = os.path.abspath(config_file)

    manager.log()
    configuration_vars = [
        ("Mypy Version", __version__),
        ("Config File", (config_file or "Default")),
        ("Configured Executable", manager.options.python_executable or "None"),
        ("Current Executable", sys.executable),
        ("Cache Dir", manager.options.cache_dir),
        ("Compiled", str(not __file__.endswith(".py"))),
        ("Exclude", manager.options.exclude),
    ]

    for conf_name, conf_value in configuration_vars:
        manager.log(f"{conf_name + ':':24}{conf_value}")

    for source in sources:
        manager.log(f"{'Found source:':24}{source}")

    # Complete list of searched paths can get very long, put them under TRACE
    for path_type, paths in manager.search_paths.asdict().items():
        if not paths:
            manager.trace(f"No {path_type}")
            continue

        manager.trace(f"{path_type}:")

        for pth in paths:
            manager.trace(f"    {pth}")

