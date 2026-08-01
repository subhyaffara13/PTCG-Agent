
def test_printoptions_thread_safety():
    # until NumPy 2.1 the printoptions state was stored in globals
    # this verifies that they are now stored in a context variable
    b = threading.Barrier(2)

    def legacy_113():
        np.set_printoptions(legacy='1.13', precision=12)
        b.wait()
        po = np.get_printoptions()
        assert po['legacy'] == '1.13'
        assert po['precision'] == 12
        orig_linewidth = po['linewidth']
        with np.printoptions(linewidth=34, legacy='1.21'):
            po = np.get_printoptions()
            assert po['legacy'] == '1.21'
            assert po['precision'] == 12
            assert po['linewidth'] == 34
        po = np.get_printoptions()
        assert po['linewidth'] == orig_linewidth
        assert po['legacy'] == '1.13'
        assert po['precision'] == 12

    def legacy_125():
        np.set_printoptions(legacy='1.25', precision=7)
        b.wait()
        po = np.get_printoptions()
        assert po['legacy'] == '1.25'
        assert po['precision'] == 7
        orig_linewidth = po['linewidth']
        with np.printoptions(linewidth=6, legacy='1.13'):
            po = np.get_printoptions()
            assert po['legacy'] == '1.13'
            assert po['precision'] == 7
            assert po['linewidth'] == 6
        po = np.get_printoptions()
        assert po['linewidth'] == orig_linewidth
        assert po['legacy'] == '1.25'
        assert po['precision'] == 7

    task1 = threading.Thread(target=legacy_113)
    task2 = threading.Thread(target=legacy_125)

    task1.start()
    task2.start()
    task1.join()
    task2.join()

