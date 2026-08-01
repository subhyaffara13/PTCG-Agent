
def alternatives(*rules):
    """Strategy that makes an AlternativeRule out of multiple possible results."""
    def _alternatives(integral):
        alts = []
        count = 0
        debug("List of Alternative Rules")
        for rule in rules:
            count = count + 1
            debug("Rule {}: {}".format(count, rule))

            result = rule(integral)
            if (result and not isinstance(result, DontKnowRule) and
                result != integral and result not in alts):
                alts.append(result)
        if len(alts) == 1:
            return alts[0]
        elif alts:
            doable = [rule for rule in alts if not rule.contains_dont_know()]
            if doable:
                return AlternativeRule(*integral, doable)
            else:
                return AlternativeRule(*integral, alts)
    return _alternatives

