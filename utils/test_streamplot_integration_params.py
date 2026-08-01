
def test_streamplot_integration_params():
    x = np.array([[10, 20], [10, 20]])
    y = np.array([[10, 10], [20, 20]])
    u = np.ones((2, 2))
    v = np.zeros((2, 2))

    err_str = "The value of integration_max_step_scale must be > 0, got -0.5"
    with pytest.raises(ValueError, match=err_str):
        plt.streamplot(x, y, u, v, integration_max_step_scale=-0.5)

    err_str = "The value of integration_max_error_scale must be > 0, got 0.0"
    with pytest.raises(ValueError, match=err_str):
        plt.streamplot(x, y, u, v, integration_max_error_scale=0.0)

