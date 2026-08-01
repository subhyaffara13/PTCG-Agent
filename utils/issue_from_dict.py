
def issue_from_dict(data):
    i = Issue(severity=data["issue_severity"])
    i.from_dict(data)
    return i

