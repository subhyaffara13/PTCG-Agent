
def test_info_method_heading():
    # info(class) should only print "Methods:" heading if methods exist

    class NoPublicMethods:
        pass

    class WithPublicMethods:
        def first_method():
            pass

    def _has_method_heading(cls):
        out = StringIO()
        np.info(cls, output=out)
        return 'Methods:' in out.getvalue()

    assert _has_method_heading(WithPublicMethods)
    assert not _has_method_heading(NoPublicMethods)

