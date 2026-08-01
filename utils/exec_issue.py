
def exec_issue():
    return bandit.Issue(
        severity=bandit.MEDIUM,
        confidence=bandit.HIGH,
        cwe=issue.Cwe.OS_COMMAND_INJECTION,
        text="Use of exec detected.",
    )


def exec_issue(level, members=""):
    if level == bandit.LOW:
        return bandit.Issue(
            severity=bandit.LOW,
            confidence=bandit.LOW,
            cwe=issue.Cwe.PATH_TRAVERSAL,
            text="Usage of tarfile.extractall(members=function(tarfile)). "
            "Make sure your function properly discards dangerous members "
            "{members}).".format(members=members),
        )
    elif level == bandit.MEDIUM:
        return bandit.Issue(
            severity=bandit.MEDIUM,
            confidence=bandit.MEDIUM,
            cwe=issue.Cwe.PATH_TRAVERSAL,
            text="Found tarfile.extractall(members=?) but couldn't "
            "identify the type of members. "
            "Check if the members were properly validated "
            "{members}).".format(members=members),
        )
    else:
        return bandit.Issue(
            severity=bandit.HIGH,
            confidence=bandit.HIGH,
            cwe=issue.Cwe.PATH_TRAVERSAL,
            text="tarfile.extractall used without any validation. "
            "Please check and discard dangerous members.",
        )

