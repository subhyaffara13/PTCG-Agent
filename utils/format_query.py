
def format_query(sql, *args):
    _formatters = {
        datetime: "'{}'".format,
        str: "'{}'".format,
        np.str_: "'{}'".format,
        bytes: "'{}'".format,
        float: "{:.8f}".format,
        int: "{:d}".format,
        type(None): lambda x: "NULL",
        np.float64: "{:.10f}".format,
        bool: "'{!s}'".format,
    }
    processed_args = []
    for arg in args:
        if isinstance(arg, float) and isna(arg):
            arg = None

        formatter = _formatters[type(arg)]
        processed_args.append(formatter(arg))

    return sql % tuple(processed_args)

