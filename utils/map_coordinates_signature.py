
def map_coordinates_signature(input, coordinates, output=None, *args, **kwds):
    return array_namespace(input, coordinates, _skip_if_dtype(output))

