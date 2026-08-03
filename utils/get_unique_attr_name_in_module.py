import re

def get_unique_attr_name_in_module(mod_traced: torch.fx.GraphModule, name: str) -> str:
    """
    Make sure the name is unique (in a module) and can represents an attr.
    """
    # Delete all characters that are illegal in a Python identifier.
    name = re.sub("[^0-9a-zA-Z_]+", "_", name)
    if name[0].isdigit():
        name = f"_{name}"
    # Now make sure it is in fact unique to the module by incrementing suffix value.
    while hasattr(mod_traced, name):
        match = re.match(r"(.*)_(\d+)$", name)
        if match is None:
            name = name + "_1"
        else:
            base, num = match.group(1, 2)
            name = f"{base}_{int(num) + 1}"

    return name

