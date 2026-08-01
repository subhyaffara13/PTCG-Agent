
def parse_xinfo_stream(response, **options):
    if isinstance(response, list):
        data = pairs_to_dict(response, decode_keys=True)
    else:
        data = {str_if_bytes(k): v for k, v in response.items()}
    if not options.get("full", False):
        first = data.get("first-entry")
        if first is not None and first[0] is not None:
            data["first-entry"] = (first[0], pairs_to_dict(first[1]))
        last = data["last-entry"]
        if last is not None and last[0] is not None:
            data["last-entry"] = (last[0], pairs_to_dict(last[1]))
    else:
        data["entries"] = {_id: pairs_to_dict(entry) for _id, entry in data["entries"]}
        if len(data["groups"]) > 0 and isinstance(data["groups"][0], list):
            data["groups"] = [
                pairs_to_dict(group, decode_keys=True) for group in data["groups"]
            ]
            for g in data["groups"]:
                if g["consumers"] and g["consumers"][0] is not None:
                    g["consumers"] = [
                        pairs_to_dict(c, decode_keys=True) for c in g["consumers"]
                    ]
        else:
            data["groups"] = [
                {str_if_bytes(k): v for k, v in group.items()}
                for group in data["groups"]
            ]
    return data

