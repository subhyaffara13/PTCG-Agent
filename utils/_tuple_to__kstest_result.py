
def _tuple_to_KstestResult(statistic, pvalue,
                           statistic_location, statistic_sign):
    return KstestResult(statistic, pvalue,
                        statistic_location=statistic_location,
                        statistic_sign=statistic_sign)

