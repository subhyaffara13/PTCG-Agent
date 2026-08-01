
def _mps_tag(obj):
    if obj.device.type == "mps":
        return "mps"

