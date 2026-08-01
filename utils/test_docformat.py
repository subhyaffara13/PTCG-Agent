
def test_docformat():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        udd = doccer.unindent_dict(doc_dict)
        formatted = doccer.docformat(docstring, udd)
        assert_equal(formatted, filled_docstring)
        single_doc = 'Single line doc %(strtest1)s'
        formatted = doccer.docformat(single_doc, doc_dict)
        # Note - initial indent of format string does not
        # affect subsequent indent of inserted parameter
        assert_equal(formatted, """Single line doc Another test
   with some indent""")

