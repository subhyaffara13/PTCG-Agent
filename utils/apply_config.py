
def apply_config(cls, kwargs, conf_dict=None):
    """Supply default values for kwargs when instantiating class

    Augments the passed kwargs, by finding entries in the config dict
    which match the classes ``.protocol`` attribute (one or more str)

    Parameters
    ----------
    cls : file system implementation
    kwargs : dict
    conf_dict : dict of dict
        Typically this is the global configuration

    Returns
    -------
    dict : the modified set of kwargs
    """
    if conf_dict is None:
        conf_dict = conf
    protos = cls.protocol if isinstance(cls.protocol, (tuple, list)) else [cls.protocol]
    kw = {}
    for proto in protos:
        # default kwargs from the current state of the config
        if proto in conf_dict:
            kw.update(conf_dict[proto])
    # explicit kwargs always win
    kw.update(**kwargs)
    kwargs = kw
    return kwargs

