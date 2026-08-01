
def evaluateRule(rule, location):
    """Return True if any of the rule's conditionsets matches the given location."""
    return any(evaluateConditions(c, location) for c in rule.conditionSets)

