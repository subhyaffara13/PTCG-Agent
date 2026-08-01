
def boolean_flag(name: str, configurable: str, set_help: str = "", unset_help: str = "") -> StrDict:
    """Helper for building basic --trait, --no-trait flags.

    Parameters
    ----------
    name : str
        The name of the flag.
    configurable : str
        The 'Class.trait' string of the trait to be set/unset with the flag
    set_help : unicode
        help string for --name flag
    unset_help : unicode
        help string for --no-name flag

    Returns
    -------
    cfg : dict
        A dict with two keys: 'name', and 'no-name', for setting and unsetting
        the trait, respectively.
    """
    # default helpstrings
    set_help = set_help or "set %s=True" % configurable
    unset_help = unset_help or "set %s=False" % configurable

    cls, trait = configurable.split(".")

    setter = {cls: {trait: True}}
    unsetter = {cls: {trait: False}}
    return {name: (setter, set_help), "no-" + name: (unsetter, unset_help)}

