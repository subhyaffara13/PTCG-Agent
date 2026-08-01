
def test_check_buttons(fig_test, fig_ref):
    widgets.CheckButtons(fig_test.subplots(), ["tea", "coffee"], [True, True])
    ax = fig_ref.add_subplot(xticks=[], yticks=[])
    ax.scatter([.15, .15], [2/3, 1/3], marker='s', transform=ax.transAxes,
               s=(plt.rcParams["font.size"] / 2) ** 2, c=["none", "none"])
    ax.scatter([.15, .15], [2/3, 1/3], marker='x', transform=ax.transAxes,
               s=(plt.rcParams["font.size"] / 2) ** 2, c=["k", "k"])
    ax.text(.25, 2/3, "tea", transform=ax.transAxes, va="center")
    ax.text(.25, 1/3, "coffee", transform=ax.transAxes, va="center")

