
def _multilines(obj):
    try:
        lines = obj.splitlines()
        return lines + [""] if obj.endswith("\n") else lines
    except AttributeError:
        # Remove the final blank space on Python 2.7
        # return json.dumps(obj, indent=True, sort_keys=True).splitlines()
        return [line.rstrip() for line in json.dumps(obj, indent=True, sort_keys=True).splitlines()]

