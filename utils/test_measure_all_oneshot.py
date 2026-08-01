
def test_measure_all_oneshot():
    random.seed(42)
    # for issue #27092
    assert measure_all_oneshot(Qubit('11')) == Qubit('11')
    assert measure_all_oneshot(Qubit('1')) == Qubit('1')
    assert measure_all_oneshot(Qubit('0')/sqrt(2) + Qubit('1')/sqrt(2)) == \
            Qubit('0')

