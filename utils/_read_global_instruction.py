
def _read_global_instruction(readline: Callable) -> tuple[str, str]:
    module = readline()[:-1].decode("utf-8")
    name = readline()[:-1].decode("utf-8")
    # Patch since torch.save default protocol is 2
    # users will be running this code in python > 3
    if (module, name) in NAME_MAPPING:
        module, name = NAME_MAPPING[(module, name)]
    elif module in IMPORT_MAPPING:
        module = IMPORT_MAPPING[module]
    return module, name

