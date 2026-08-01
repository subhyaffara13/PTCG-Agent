
def test_unindent_dict():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        d2 = doccer.unindent_dict(doc_dict)
    assert_equal(d2['strtest1'], doc_dict['strtest1'])
    assert_equal(d2['strtest2'], doc_dict['strtest2'])
    assert_equal(d2['strtest3'], doc_dict['strtest1'])

