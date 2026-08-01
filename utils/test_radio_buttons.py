
def test_radio_buttons(fig_test, fig_ref):
    widgets.RadioButtons(fig_test.subplots(), ["tea", "coffee"])
    ax = fig_ref.add_subplot(xticks=[], yticks=[])
    ax.scatter([.15, .15], [2/3, 1/3], transform=ax.transAxes,
               s=(plt.rcParams["font.size"] / 2) ** 2, c=["C0", "none"])
    ax.text(.25, 2/3, "tea", transform=ax.transAxes, va="center")
    ax.text(.25, 1/3, "coffee", transform=ax.transAxes, va="center")

