
def python_parser_only(request):
    """
    Fixture all of the CSV parsers using the Python engine.
    """
    return request.param()

