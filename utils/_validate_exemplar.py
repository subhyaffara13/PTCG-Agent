
def _validate_exemplar(exemplar):
    """Raises ValueError if the exemplar is invalid."""
    runes = 0
    for k, v in exemplar.items():
        _validate_labelname(k)
        runes += len(k)
        runes += len(v)
    if runes > 128:
        raise ValueError('Exemplar labels have %d UTF-8 characters, exceeding the limit of 128')

