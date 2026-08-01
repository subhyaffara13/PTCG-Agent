
def parse_stream_list(response, **options):
    if response is None:
        return None
    data = []
    for r in response:
        if r is not None:
            if "claim_min_idle_time" in options:
                data.append((r[0], pairs_to_dict(r[1]), *r[2:]))
            else:
                data.append((r[0], pairs_to_dict(r[1])))
        else:
            data.append((None, None))
    return data

