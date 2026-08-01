
def test_algorithm_supports_corner_mask(algorithm):
    z = np.array([[1.0, 2.0], [3.0, 4.0]])

    # All algorithms support corner_mask=False
    plt.contourf(z, algorithm=algorithm, corner_mask=False)

    # Only some algorithms support corner_mask=True
    if algorithm != 'mpl2005':
        plt.contourf(z, algorithm=algorithm, corner_mask=True)
    else:
        with pytest.raises(ValueError):
            plt.contourf(z, algorithm=algorithm, corner_mask=True)

