import re

def _old_installed_distributions(local: bool):
    list_args = ["list"]
    if local:
        list_args.append("--local")
    result = call(*list_args)

    # result is of the form:
    # <package_name> (<version>)
    #
    # or, if editable
    # <package_name> (<version>, <location>)
    #
    # or, could be a warning line

    ret = {}

    pattern = re.compile(r"(.*) \((.*)\)")

    for line in result.strip().split("\n"):
        match = re.match(pattern, line)

        if match:
            name, paren = match.groups()
            version, location = (paren.split(", ") + [None])[:2]

            ret[name] = Distribution(name, version, location)
        else:
            # This is a warning line or some other output
            pass

    return ret

