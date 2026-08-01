
def test_Poly3DCollection_init_value_error():
    # smoke test to ensure the input check works
    # GH#26420
    with pytest.raises(ValueError,
                       match='You must provide facecolors, edgecolors, '
                        'or both for shade to work.'):
        poly = np.array([[0, 0, 1], [0, 1, 1], [0, 0, 0]], float)
        c = art3d.Poly3DCollection([poly], shade=True)

