
def _check_invalid_requirement(req):
    if os.path.sep in req:
        add_msg = "It looks like a path."
        if os.path.exists(req):
            add_msg += " It does exist."
        else:
            add_msg += " File '%s' does not exist." % (req)
    elif "=" in req and not any(op in req for op in operators):
        add_msg = "= is not a valid operator. Did you mean == ?"
    else:
        add_msg = traceback.format_exc()
    raise PipError("Invalid requirement: '%s'\n%s" % (req, add_msg))

