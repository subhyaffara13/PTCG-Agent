
def test_ecdf(fig_test, fig_ref):
    data = np.array([0, -np.inf, -np.inf, np.inf, 1, 1, 2])
    weights = range(len(data))
    axs_test = fig_test.subplots(1, 2)
    for ax, orientation in zip(axs_test, ["vertical", "horizontal"]):
        l0 = ax.ecdf(data, orientation=orientation)
        l1 = ax.ecdf("d", "w", data={"d": np.ma.array(data), "w": weights},
                     orientation=orientation,
                     complementary=True, compress=True, ls=":")
        assert len(l0.get_xdata()) == (~np.isnan(data)).sum() + 1
        assert len(l1.get_xdata()) == len({*data[~np.isnan(data)]}) + 1
    axs_ref = fig_ref.subplots(1, 2)
    axs_ref[0].plot([-np.inf, -np.inf, -np.inf, 0, 1, 1, 2, np.inf],
                    np.arange(8) / 7, ds="steps-post")
    axs_ref[0].plot([-np.inf, 0, 1, 2, np.inf, np.inf],
                    np.array([21, 20, 18, 14, 3, 0]) / 21,
                    ds="steps-pre", ls=":")
    axs_ref[1].plot(np.arange(8) / 7,
                    [-np.inf, -np.inf, -np.inf, 0, 1, 1, 2, np.inf],
                    ds="steps-pre")
    axs_ref[1].plot(np.array([21, 20, 18, 14, 3, 0]) / 21,
                    [-np.inf, 0, 1, 2, np.inf, np.inf],
                    ds="steps-post", ls=":")

