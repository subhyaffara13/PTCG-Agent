
def float_or_none(response):
    if response is None:
        return None
    return float(response)

