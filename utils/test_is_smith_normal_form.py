
def test_is_smith_normal_form():

    snf_examples = [
        DM([[0, 0], [0, 0]], ZZ),
        DM([[1, 0], [0, 0]], ZZ),
        DM([[1, 0], [0, 1]], ZZ),
        DM([[1, 0], [0, 2]], ZZ),
    ]

    non_snf_examples = [
        DM([[0, 1], [0, 0]], ZZ),
        DM([[0, 0], [0, 1]], ZZ),
        DM([[2, 0], [0, 3]], ZZ),
    ]

    for m in snf_examples:
        assert is_smith_normal_form(m) is True

    for m in non_snf_examples:
        assert is_smith_normal_form(m) is False

