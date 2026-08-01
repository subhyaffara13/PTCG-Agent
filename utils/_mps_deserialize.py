
def _mps_deserialize(obj, location):
    if location.startswith("mps"):
        return obj.mps()

