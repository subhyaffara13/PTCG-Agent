
def test_nostrictio_contentsfmode():
    bench(False, dill.CONTENTS_FMODE, True)
    teardown_module()

