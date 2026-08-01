
def remove_ticks_and_titles(figure):
    figure.suptitle("")
    null_formatter = ticker.NullFormatter()
    def remove_ticks(ax):
        """Remove ticks in *ax* and all its child Axes."""
        ax.set_title("")
        ax.xaxis.set_major_formatter(null_formatter)
        ax.xaxis.set_minor_formatter(null_formatter)
        ax.yaxis.set_major_formatter(null_formatter)
        ax.yaxis.set_minor_formatter(null_formatter)
        try:
            ax.zaxis.set_major_formatter(null_formatter)
            ax.zaxis.set_minor_formatter(null_formatter)
        except AttributeError:
            pass
        for child in ax.child_axes:
            remove_ticks(child)
    for ax in figure.get_axes():
        remove_ticks(ax)

