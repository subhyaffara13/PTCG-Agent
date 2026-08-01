
def _get_ttest_ci(ttest):
    # get a function that returns the CI bounds of provided `ttest`
    def ttest_ci(*args, **kwargs):
        res = ttest(*args, **kwargs)
        return res.confidence_interval()
    return ttest_ci

