
def block_maker(request):
    """
    Fixture to test both the internal new_block and pseudo-public make_block.
    """
    return request.param

