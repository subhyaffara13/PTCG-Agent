
def zip_type_and_name(types: list[str], names: list[str]) -> list[str]:
    return [typ + " " + name for typ, name in zip(types, names)]

