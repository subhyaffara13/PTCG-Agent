
def test_cannot_assign_data():
    a = np.arange(10)
    b = np.linspace(0, 1, 10)
    with pytest.raises(AttributeError):
        a.data = b.data

