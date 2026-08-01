
def _cpu_tag(obj):
    if obj.device.type == "cpu":
        return "cpu"

