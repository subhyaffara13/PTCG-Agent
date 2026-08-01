
def parse_geosearch_generic_unified(response, **options):
    """
    Parse GEOSEARCH/GEORADIUS responses using tuple coordinates.
    """
    try:
        if options["store"] or options["store_dist"]:
            return response
    except KeyError:
        return response

    response_list = response if isinstance(response, list) else [response]

    if not options["withdist"] and not options["withcoord"] and not options["withhash"]:
        return response_list

    cast = {
        "withdist": float,
        "withcoord": lambda ll: (float(ll[0]), float(ll[1])),
        "withhash": int,
    }
    funcs = [lambda x: x]
    funcs += [cast[o] for o in ["withdist", "withhash", "withcoord"] if options[o]]
    return [list(map(lambda fv: fv[0](fv[1]), zip(funcs, r))) for r in response_list]

