
def _config_inited(app, config):
    # Check for srcset hidpi images
    for i, size in enumerate(app.config.mathmpl_srcset):
        if size[-1] == 'x':  # "2x" = "2.0"
            try:
                float(size[:-1])
            except ValueError:
                raise ConfigError(
                    f'Invalid value for mathmpl_srcset parameter: {size!r}. '
                    'Must be a list of strings with the multiplicative '
                    'factor followed by an "x".  e.g. ["2.0x", "1.5x"]')
        else:
            raise ConfigError(
                f'Invalid value for mathmpl_srcset parameter: {size!r}. '
                'Must be a list of strings with the multiplicative '
                'factor followed by an "x".  e.g. ["2.0x", "1.5x"]')

