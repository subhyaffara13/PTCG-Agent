
def format_alias(name, aliases):
    source, command = aliases[name]
    if source == config_file('global'):
        source = '--global-config '
    elif source == config_file('user'):
        source = '--user-config '
    elif source == config_file('local'):
        source = ''
    else:
        source = f'--filename={source!r}'
    return source + name + ' ' + command

