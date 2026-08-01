
def test_cc_visit(code, number_of_blocks, diff, lookfor):
    code = dedent(code)

    blocks = cc_visit(code)
    assert isinstance(blocks, list)
    assert len(blocks) == number_of_blocks

    with_inner_blocks = add_inner_blocks(blocks)
    names = set(map(operator.attrgetter('name'), with_inner_blocks))
    assert len(with_inner_blocks) - len(blocks) == diff
    assert lookfor in names

