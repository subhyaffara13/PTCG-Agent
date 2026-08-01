
def test_set_codes(idx):
    # side note - you probably wouldn't want to use levels and codes
    # directly like this - but it is possible.
    codes = idx.codes
    major_codes, minor_codes = codes
    major_codes = [(x + 1) % 3 for x in major_codes]
    minor_codes = [(x + 1) % 1 for x in minor_codes]
    new_codes = [major_codes, minor_codes]

    # changing codes w/o mutation
    ind2 = idx.set_codes(new_codes)
    assert_matching(ind2.codes, new_codes)
    assert_matching(idx.codes, codes)

    # codes changing specific level w/o mutation
    ind2 = idx.set_codes(new_codes[0], level=0)
    assert_matching(ind2.codes, [new_codes[0], codes[1]])
    assert_matching(idx.codes, codes)

    ind2 = idx.set_codes(new_codes[1], level=1)
    assert_matching(ind2.codes, [codes[0], new_codes[1]])
    assert_matching(idx.codes, codes)

    # codes changing multiple levels w/o mutation
    ind2 = idx.set_codes(new_codes, level=[0, 1])
    assert_matching(ind2.codes, new_codes)
    assert_matching(idx.codes, codes)

    # label changing for levels of different magnitude of categories
    ind = MultiIndex.from_tuples([(0, i) for i in range(130)])
    new_codes = range(129, -1, -1)
    expected = MultiIndex.from_tuples([(0, i) for i in new_codes])

    # [w/o mutation]
    result = ind.set_codes(codes=new_codes, level=1)
    assert result.equals(expected)

