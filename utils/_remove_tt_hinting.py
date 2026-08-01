
def _remove_TTHinting(font):
    for tag in ("cvar", "cvt ", "fpgm", "prep"):
        if tag in font:
            del font[tag]
    maxp = font["maxp"]
    for attr in (
        "maxTwilightPoints",
        "maxStorage",
        "maxFunctionDefs",
        "maxInstructionDefs",
        "maxStackElements",
        "maxSizeOfInstructions",
    ):
        setattr(maxp, attr, 0)
    maxp.maxZones = 1
    font["glyf"].removeHinting()

