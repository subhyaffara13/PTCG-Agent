
def _is_visit_pair(obj):
    return (isinstance(obj, tuple)
            and len(obj) == 2
            and isinstance(obj[0], (int, str)))

