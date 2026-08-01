
def flagSupports(newFlag, oldFlag):
    return (
        (oldFlag & flagOnCurve) == (newFlag & flagOnCurve)
        and flagFits(newFlag, oldFlag, flagXsame | flagXShort)
        and flagFits(newFlag, oldFlag, flagYsame | flagYShort)
    )

