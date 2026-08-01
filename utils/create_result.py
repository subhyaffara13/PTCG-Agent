
def create_result(issue, rules, rule_indices):
    issue_dict = issue.as_dict()

    rule, rule_index = create_or_find_rule(issue_dict, rules, rule_indices)

    physical_location = om.PhysicalLocation(
        artifact_location=om.ArtifactLocation(
            uri=to_uri(issue_dict["filename"])
        )
    )

    add_region_and_context_region(
        physical_location,
        issue_dict["line_range"],
        issue_dict["col_offset"],
        issue_dict["end_col_offset"],
        issue_dict["code"],
    )

    return om.Result(
        rule_id=rule.id,
        rule_index=rule_index,
        message=om.Message(text=issue_dict["issue_text"]),
        level=level_from_severity(issue_dict["issue_severity"]),
        locations=[om.Location(physical_location=physical_location)],
        properties={
            "issue_confidence": issue_dict["issue_confidence"],
            "issue_severity": issue_dict["issue_severity"],
        },
    )

