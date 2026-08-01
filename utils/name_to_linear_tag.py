
def name_to_linear_tag(name):
    return ".".join([n for n in name.split(".") if ((n not in ["model", "layers"]) and (not n.isnumeric()))])

