
def set_use_numexpr(v: bool = True) -> None:
    # set/unset to use numexpr
    global USE_NUMEXPR
    if NUMEXPR_INSTALLED:
        if np_version_gt2_3 and not ne_gt_211:
            # incompatibility of numexpr 2.10 with newer pandas resulting in wrong data
            # https://github.com/pandas-dev/pandas/issues/63320
            USE_NUMEXPR = False
        else:
            USE_NUMEXPR = v

    # choose what we are going to do
    global _evaluate, _where

    _evaluate = _evaluate_numexpr if USE_NUMEXPR else _evaluate_standard
    _where = _where_numexpr if USE_NUMEXPR else _where_standard

