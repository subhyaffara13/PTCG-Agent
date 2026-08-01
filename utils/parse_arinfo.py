
def parse_arinfo(response, **options):
    if isinstance(response, list):
        return pairs_to_dict(response, decode_keys=True)
    return {str_if_bytes(k): v for k, v in response.items()}

