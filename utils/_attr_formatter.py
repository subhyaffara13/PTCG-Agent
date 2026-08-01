
def _attr_formatter(name):
    return property(lambda self: _format_time(getattr(self, name)))

