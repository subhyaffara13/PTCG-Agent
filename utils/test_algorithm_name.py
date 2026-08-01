
def test_algorithm_name(algorithm, klass):
    z = np.array([[1.0, 2.0], [3.0, 4.0]])
    if klass is not None:
        cs = plt.contourf(z, algorithm=algorithm)
        assert isinstance(cs._contour_generator, klass)
    else:
        with pytest.raises(ValueError):
            plt.contourf(z, algorithm=algorithm)

