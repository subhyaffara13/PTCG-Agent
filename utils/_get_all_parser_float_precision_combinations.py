
def _get_all_parser_float_precision_combinations():
    """
    Return all allowable parser and float precision
    combinations and corresponding ids.
    """
    params = []
    ids = []
    for parser, parser_id in zip(_all_parsers, _all_parser_ids):
        if hasattr(parser, "values"):
            # Wrapped in pytest.param, get the actual parser back
            parser = parser.values[0]
        for precision in parser.float_precision_choices:
            # Re-wrap in pytest.param for pyarrow
            mark = (
                [
                    pytest.mark.single_cpu,
                    pytest.mark.skipif(
                        not HAS_PYARROW, reason="pyarrow is not installed"
                    ),
                ]
                if parser.engine == "pyarrow"
                else ()
            )
            param = pytest.param((parser(), precision), marks=mark)
            params.append(param)
            ids.append(f"{parser_id}-{precision}")

    return {"params": params, "ids": ids}

