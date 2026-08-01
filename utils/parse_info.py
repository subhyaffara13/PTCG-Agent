
def parse_info(response):
    """Parse the result of Redis's INFO command into a Python dict"""
    info = {}
    response = str_if_bytes(response)

    def get_value(value):
        if "," not in value and "=" not in value:
            try:
                if "." in value:
                    return float(value)
                else:
                    return int(value)
            except ValueError:
                return value
        elif "=" not in value:
            return [get_value(v) for v in value.split(",") if v]
        else:
            sub_dict = {}
            for item in value.split(","):
                if not item:
                    continue
                if "=" in item:
                    k, v = item.rsplit("=", 1)
                    sub_dict[k] = get_value(v)
                else:
                    sub_dict[item] = True
            return sub_dict

    for line in response.splitlines():
        if line and not line.startswith("#"):
            if line.find(":") != -1:
                # Split, the info fields keys and values.
                # Note that the value may contain ':'. but the 'host:'
                # pseudo-command is the only case where the key contains ':'
                key, value = line.split(":", 1)
                if key == "cmdstat_host":
                    key, value = line.rsplit(":", 1)

                if key == "module":
                    # Hardcode a list for key 'modules' since there could be
                    # multiple lines that started with 'module'
                    info.setdefault("modules", []).append(get_value(value))
                else:
                    info[key] = get_value(value)
            else:
                # if the line isn't splittable, append it to the "__raw__" key
                info.setdefault("__raw__", []).append(line)

    return info

