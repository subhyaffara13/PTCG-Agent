
def add_results(issues, run):
    if run.results is None:
        run.results = []

    rules = {}
    rule_indices = {}
    for issue in issues:
        result = create_result(issue, rules, rule_indices)
        run.results.append(result)

    if len(rules) > 0:
        run.tool.driver.rules = list(rules.values())

