
def show_version_verbose(config: Config) -> None:
    """Show verbose pytest version installation, including plugins."""
    sys.stdout.write(
        f"This is pytest version {pytest.__version__}, imported from {pytest.__file__}\n"
    )
    plugininfo = getpluginversioninfo(config)
    if plugininfo:
        for line in plugininfo:
            sys.stdout.write(line + "\n")

