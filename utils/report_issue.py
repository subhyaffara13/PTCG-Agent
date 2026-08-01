
def report_issue(check, name):
    return issue.Issue(
        severity=check.get("level", "MEDIUM"),
        confidence="HIGH",
        cwe=check.get("cwe", issue.Cwe.NOTSET),
        text=check["message"].replace("{name}", name),
        ident=name,
        test_id=check.get("id", "LEGACY"),
    )

