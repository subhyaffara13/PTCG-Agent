
def test_nostrictio_filefmode():
    bench(False, dill.FILE_FMODE, False)
    teardown_module()

