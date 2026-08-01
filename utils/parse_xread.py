
def parse_xread(response, **options):
    if response is None:
        return []
    return [[r[0], parse_stream_list(r[1], **options)] for r in response]

