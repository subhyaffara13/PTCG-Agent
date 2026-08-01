
def _makedist(**attrs):
    dist = Distribution(attrs)
    dist.parse_config_files()
    return dist

