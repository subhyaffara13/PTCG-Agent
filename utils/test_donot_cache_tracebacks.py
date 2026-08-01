
def test_donot_cache_tracebacks():

    class SomeObject:
        pass

    def inner():
        x = SomeObject()
        fig = mfigure.Figure()
        ax = fig.subplots()
        fig.text(.5, .5, 'aardvark', family='doesnotexist')
        with BytesIO() as out:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                fig.savefig(out, format='raw')

    inner()

    for obj in gc.get_objects():
        if isinstance(obj, SomeObject):
            pytest.fail("object from inner stack still alive")

