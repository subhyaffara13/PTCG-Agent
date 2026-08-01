
def create_or_find_rule(issue_dict, rules, rule_indices):
    rule_id = issue_dict["test_id"]
    if rule_id in rules:
        return rules[rule_id], rule_indices[rule_id]

    rule = om.ReportingDescriptor(
        id=rule_id,
        name=issue_dict["test_name"],
        help_uri=docs_utils.get_url(rule_id),
        properties={
            "tags": [
                "security",
                f"external/cwe/cwe-{issue_dict['issue_cwe'].get('id')}",
            ],
            "precision": issue_dict["issue_confidence"].lower(),
        },
    )

    index = len(rules)
    rules[rule_id] = rule
    rule_indices[rule_id] = index
    return rule, index

