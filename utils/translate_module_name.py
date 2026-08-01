
def translate_module_name(module: str, relative: int) -> tuple[str, int]:
    for pkg in VENDOR_PACKAGES:
        for alt in "six.moves", "six":
            substr = f"{pkg}.{alt}"
            if module.endswith("." + substr) or (module == substr and relative):
                return alt, 0
            if "." + substr + "." in module:
                return alt + "." + module.partition("." + substr + ".")[2], 0
    return module, relative

