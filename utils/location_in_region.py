
def locationInRegion(location: SimpleLocationDict, region: Region) -> bool:
    for name, value in location.items():
        if name not in region:
            return False
        regionValue = region[name]
        if isinstance(regionValue, (float, int)):
            if value != regionValue:
                return False
        else:
            if value not in regionValue:
                return False
    return True

