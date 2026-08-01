
def _sample_odds_ratio_ci(table, confidence_level=0.95,
                          alternative='two-sided'):
    oddsratio = _sample_odds_ratio(table)
    log_or = np.log(oddsratio)
    se = np.sqrt((1/table).sum())
    if alternative == 'less':
        z = ndtri(confidence_level)
        loglow = -np.inf
        loghigh = log_or + z*se
    elif alternative == 'greater':
        z = ndtri(confidence_level)
        loglow = log_or - z*se
        loghigh = np.inf
    else:
        # alternative is 'two-sided'
        z = ndtri(0.5*confidence_level + 0.5)
        loglow = log_or - z*se
        loghigh = log_or + z*se

    return np.exp(loglow), np.exp(loghigh)

