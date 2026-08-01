
def test_hist_log_2(fig_test, fig_ref):
    axs_test = fig_test.subplots(2, 3)
    axs_ref = fig_ref.subplots(2, 3)
    for i, histtype in enumerate(["bar", "step", "stepfilled"]):
        # Set log scale, then call hist().
        axs_test[0, i].set_yscale("log")
        axs_test[0, i].hist(1, 1, histtype=histtype)
        # Call hist(), then set log scale.
        axs_test[1, i].hist(1, 1, histtype=histtype)
        axs_test[1, i].set_yscale("log")
        # Use hist(..., log=True).
        for ax in axs_ref[:, i]:
            ax.hist(1, 1, log=True, histtype=histtype)

