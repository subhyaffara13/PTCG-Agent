
def regionInRegion(region: Region, superRegion: Region) -> bool:
    for name, value in region.items():
        if not name in superRegion:
            return False
        superValue = superRegion[name]
        if isinstance(superValue, (float, int)):
            if value != superValue:
                return False
        else:
            if value not in superValue:
                return False
    return True

