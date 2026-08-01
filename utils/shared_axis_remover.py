
def shared_axis_remover(request):
    def _helper_x(ax):
        ax2 = ax.twinx()
        ax2.remove()
        ax.set_xlim(0, 15)
        r = ax.xaxis.get_major_locator()()
        assert r[-1] > 14

    def _helper_y(ax):
        ax2 = ax.twiny()
        ax2.remove()
        ax.set_ylim(0, 15)
        r = ax.yaxis.get_major_locator()()
        assert r[-1] > 14

    return {"x": _helper_x, "y": _helper_y}[request.param]

