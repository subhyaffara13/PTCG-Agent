
def open_ufo(path):
    if hasattr(ufo_module.Font, "open"):  # ufoLib2
        return ufo_module.Font.open(path)
    return ufo_module.Font(path)  # defcon

