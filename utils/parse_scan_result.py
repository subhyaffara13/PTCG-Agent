
def parse_scan_result(command, res, **options):
    cursors = {}
    ret = []
    for node_name, response in res.items():
        cursor, r = parse_scan(response, **options)
        cursors[node_name] = cursor
        ret += r

    return cursors, ret

