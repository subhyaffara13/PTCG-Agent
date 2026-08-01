
def test_nat_doc_strings(compare):
    # see gh-17327
    #
    # The docstrings for overlapping methods should match.
    klass, method = compare
    klass_doc = getattr(klass, method).__doc__

    if klass == Timestamp and method == "isoformat":
        pytest.skip(
            "Ignore differences with Timestamp.isoformat() as they're intentional"
        )

    if method == "to_numpy":
        # GH#44460 can return either dt64 or td64 depending on dtype,
        #  different docstring is intentional
        pytest.skip(f"different docstring for {method} is intentional")

    nat_doc = getattr(NaT, method).__doc__
    assert klass_doc == nat_doc

