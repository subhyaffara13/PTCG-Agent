
def export_rewrite_case(**kwargs):
    def wrapper(m):
        configs = kwargs

        parent = configs.pop("parent")
        if not isinstance(parent, ExportCase):
            raise AssertionError(f"expected ExportCase, got {type(parent)}")
        key = parent.name
        if key not in _EXAMPLE_REWRITE_CASES:
            _EXAMPLE_REWRITE_CASES[key] = []

        configs["example_args"] = parent.example_args
        case = _make_export_case(m, to_snake_case(m.__name__), configs)
        _EXAMPLE_REWRITE_CASES[key].append(case)
        return case

    return wrapper

