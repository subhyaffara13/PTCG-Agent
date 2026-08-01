
def get_f2py_modulename(source):
    name = None
    with open(source) as f:
        for line in f:
            m = _f2py_module_name_match(line)
            if m:
                if _f2py_user_module_name_match(line):  # skip *__user__* names
                    continue
                name = m.group('name')
                break
    return name

