
def test_doc_note():
    def method(self):
        """This docstring

        Has multiple lines

        And notes

        Notes
        -----
        original note
        """
        pass

    expected_doc = """This docstring

Has multiple lines

And notes

Notes
-----
note

original note"""

    assert_equal(np.ma.core.doc_note(method.__doc__, "note"), expected_doc)

