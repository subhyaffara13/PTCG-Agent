
def six_moves_transform():
    code = dedent(
        """
    class Moves(object):
    {}
    moves = Moves()
    """
    ).format(_indent(_IMPORTS, "    "))
    module = AstroidBuilder(AstroidManager()).string_build(code)
    module.name = "six.moves"
    return module

