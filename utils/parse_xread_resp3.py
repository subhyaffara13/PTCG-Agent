
def parse_xread_resp3(response, **options):
    if response is None:
        return {}
    return {
        key: [parse_stream_list(value, **options)] for key, value in response.items()
    }

