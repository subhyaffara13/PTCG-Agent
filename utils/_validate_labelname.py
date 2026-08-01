
def _validate_labelname(l):
    """Raises ValueError if the provided name is not a valid label name.
    
    This check uses the global legacy validation setting to determine the validation scheme.
    """
    if get_legacy_validation():
        if not METRIC_LABEL_NAME_RE.match(l):
            raise ValueError('Invalid label metric name: ' + l)
        if RESERVED_METRIC_LABEL_NAME_RE.match(l):
            raise ValueError('Reserved label metric name: ' + l)
    else:
        try:
            l.encode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('Invalid label metric name: ' + l)
        if RESERVED_METRIC_LABEL_NAME_RE.match(l):
            raise ValueError('Reserved label metric name: ' + l)

