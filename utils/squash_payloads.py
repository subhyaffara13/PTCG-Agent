
def squash_payloads(queue):
    squashed = {}
    if len(queue) == 0:
        return squashed
    if len(queue) == 1:
        return {"key": {"item": queue[0], "count": 1}}

    for item in queue:
        url = item["url"]
        alert_type = item["alert_type"]
        _key = (url, alert_type)

        if _key in squashed:
            squashed[_key]["count"] += 1
            # Merge the payloads

        else:
            squashed[_key] = {"item": item, "count": 1}

    return squashed

