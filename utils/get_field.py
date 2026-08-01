
def get_field(config, name):
    if name == "num_warps":
        return config.num_warps
    elif name == "num_stages":
        return config.num_stages
    elif name == "waves_per_eu":
        return config.kwargs.get(name, int(8 // config.num_warps))
    else:
        return config.kwargs.get(name, None)

