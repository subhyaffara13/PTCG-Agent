
def filter_platform_specific(lines: list[str]) -> list[str]:
    return [l for l in lines if '"size":' not in l and '"hash":' not in l]

