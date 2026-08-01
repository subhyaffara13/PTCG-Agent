
def test_setitem_preserves_views():
    # GH#28150, see also extension test of the same name
    arr = NumpyExtensionArray(np.array([1, 2, 3]))
    view1 = arr.view()
    view2 = arr[:]
    view3 = np.asarray(arr)

    arr[0] = 9
    assert view1[0] == 9
    assert view2[0] == 9
    assert view3[0] == 9

    arr[-1] = 2.5
    view1[-1] = 5
    assert arr[-1] == 5

