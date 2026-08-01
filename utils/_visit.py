
def _visit(self, func):
    """Recurse down from self, if type of an object is ot.Device,
    call func() on it.  Works on otData-style classes."""

    if type(self) == ot.Device:
        func(self)

    elif isinstance(self, list):
        for that in self:
            _visit(that, func)

    elif hasattr(self, "getConverters") and not hasattr(self, "postRead"):
        for conv in self.getConverters():
            that = getattr(self, conv.name, None)
            if that is not None:
                _visit(that, func)

    elif isinstance(self, ot.ValueRecord):
        for that in self.__dict__.values():
            _visit(that, func)

