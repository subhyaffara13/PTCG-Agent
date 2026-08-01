
def parse_zmscore(response, **options):
    # zmscore: list of scores (double precision floating point number) or nil
    return [float(score) if score is not None else None for score in response]

