
def _fit_determine_optimizer(optimizer):
    if not callable(optimizer) and isinstance(optimizer, str):
        if not optimizer.startswith('fmin_'):
            optimizer = "fmin_"+optimizer
        if optimizer == 'fmin_':
            optimizer = 'fmin'
        try:
            optimizer = getattr(optimize, optimizer)
        except AttributeError as e:
            raise ValueError(f"{optimizer} is not a valid optimizer") from e
    return optimizer

