
def get_options_by_dest(optparse_options, skip_editable=False):
    """
    Given an optparse Values object, return a {dest: value} mapping.
    """
    options_by_dest = optparse_options.__dict__
    options = {}
    for dest in OPT_BY_OPTIONS_DEST:
        if skip_editable and dest == "editables":
            continue
        value = options_by_dest.get(dest)
        if value:
            options[dest] = value
    return options

