
def test_unindent():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        assert_equal(doccer.unindent_string(param_doc1), param_doc1)
        assert_equal(doccer.unindent_string(param_doc2), param_doc2)
        assert_equal(doccer.unindent_string(param_doc3), param_doc1)

