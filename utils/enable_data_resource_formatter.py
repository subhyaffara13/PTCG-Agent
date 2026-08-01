
def enable_data_resource_formatter(enable: bool) -> None:
    if "IPython" not in sys.modules:
        # definitely not in IPython
        return
    from IPython import get_ipython

    # error: Call to untyped function "get_ipython" in typed context
    ip = get_ipython()  # type: ignore[no-untyped-call]
    if ip is None:
        # still not in IPython
        return

    formatters = ip.display_formatter.formatters
    mimetype = "application/vnd.dataresource+json"

    if enable:
        if mimetype not in formatters:
            # define tableschema formatter
            from IPython.core.formatters import BaseFormatter
            from traitlets import ObjectName

            class TableSchemaFormatter(BaseFormatter):
                print_method = ObjectName("_repr_data_resource_")
                _return_type = (dict,)

            # register it:
            formatters[mimetype] = TableSchemaFormatter()
        # enable it if it's been disabled:
        formatters[mimetype].enabled = True
    # unregister tableschema mime-type
    elif mimetype in formatters:
        formatters[mimetype].enabled = False

