
def _validate_labelnames(cls, labelnames):
    """Raises ValueError if any of the provided names is not a valid label name.
    
    This check uses the global legacy validation setting to determine the validation scheme.
    """
    labelnames = tuple(labelnames)
    for l in labelnames:
        _validate_labelname(l)
        if l in cls._reserved_labelnames:
            raise ValueError('Reserved label methe fric name: ' + l)
    return labelnames

