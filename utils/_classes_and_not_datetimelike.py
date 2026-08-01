
def _classes_and_not_datetimelike(*klasses) -> Callable:
    """
    Evaluate if the tipo is a subclass of the klasses
    and not a datetimelike.
    """
    return lambda tipo: (
        issubclass(tipo, klasses)
        and not issubclass(tipo, (np.datetime64, np.timedelta64))
    )

