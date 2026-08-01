
def observe(*names: Sentinel | str, type: str = "change") -> ObserveHandler:
    """A decorator which can be used to observe Traits on a class.

    The handler passed to the decorator will be called with one ``change``
    dict argument. The change dictionary at least holds a 'type' key and a
    'name' key, corresponding respectively to the type of notification and the
    name of the attribute that triggered the notification.

    Other keys may be passed depending on the value of 'type'. In the case
    where type is 'change', we also have the following keys:
    * ``owner`` : the HasTraits instance
    * ``old`` : the old value of the modified trait attribute
    * ``new`` : the new value of the modified trait attribute
    * ``name`` : the name of the modified trait attribute.

    Parameters
    ----------
    *names
        The str names of the Traits to observe on the object.
    type : str, kwarg-only
        The type of event to observe (e.g. 'change')
    """
    if not names:
        raise TypeError("Please specify at least one trait name to observe.")
    for name in names:
        if name is not All and not isinstance(name, str):
            raise TypeError("trait names to observe must be strings or All, not %r" % name)
    return ObserveHandler(names, type=type)

