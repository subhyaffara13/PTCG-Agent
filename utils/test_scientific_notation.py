
def test_scientific_notation():
    """Test that both 'e' and 'E' are parsed correctly."""
    data = StringIO(

            "1.0e-1,2.0E1,3.0\n"
            "4.0e-2,5.0E-1,6.0\n"
            "7.0e-3,8.0E1,9.0\n"
            "0.0e-4,1.0E-1,2.0"

    )
    expected = np.array(
        [[0.1, 20., 3.0], [0.04, 0.5, 6], [0.007, 80., 9], [0, 0.1, 2]]
    )
    assert_array_equal(np.loadtxt(data, delimiter=","), expected)

