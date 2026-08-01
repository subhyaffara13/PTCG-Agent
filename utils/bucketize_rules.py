
def bucketizeRules(self, c, rules, bucketKeys):
    buckets = {}
    for seq, recs in rules:
        buckets.setdefault(seq[c.InputIdx][0], []).append(
            (tuple(s[1 if i == c.InputIdx else 0 :] for i, s in enumerate(seq)), recs)
        )

    rulesets = []
    for firstGlyph in bucketKeys:
        if firstGlyph not in buckets:
            rulesets.append(None)
            continue
        thisRules = []
        for seq, recs in buckets[firstGlyph]:
            rule = getattr(ot, c.Rule)()
            c.SetRuleData(rule, seq)
            setattr(rule, c.Type + "Count", len(recs))
            setattr(rule, c.LookupRecord, recs)
            thisRules.append(rule)

        ruleset = getattr(ot, c.RuleSet)()
        setattr(ruleset, c.Rule, thisRules)
        setattr(ruleset, c.RuleCount, len(thisRules))
        rulesets.append(ruleset)

    setattr(self, c.RuleSet, rulesets)
    setattr(self, c.RuleSetCount, len(rulesets))

