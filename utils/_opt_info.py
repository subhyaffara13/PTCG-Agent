
def _opt_info():
    """
    Returns a string containing the CPU features supported
    by the current build.

    The format of the string can be explained as follows:
        - Dispatched features supported by the running machine end with `*`.
        - Dispatched features not supported by the running machine
          end with `?`.
        - Remaining features represent the baseline.

    Returns:
        str: A formatted string indicating the supported CPU features.
    """
    from numpy._core._multiarray_umath import (
        __cpu_baseline__,
        __cpu_dispatch__,
        __cpu_features__,
    )

    if len(__cpu_baseline__) == 0 and len(__cpu_dispatch__) == 0:
        return ''

    enabled_features = ' '.join(__cpu_baseline__)
    for feature in __cpu_dispatch__:
        if __cpu_features__[feature]:
            enabled_features += f" {feature}*"
        else:
            enabled_features += f" {feature}?"

    return enabled_features

