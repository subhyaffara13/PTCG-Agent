
def pyarrow_parser_only(request):
    """
    Fixture all of the CSV parsers using the Pyarrow engine.
    """
    return request.param()

