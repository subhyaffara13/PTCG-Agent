
def _add_axis_labels_title(plot, xlabel, ylabel, title):
    """Helper function to add axes labels and a title to stats plots."""
    try:
        if hasattr(plot, 'set_title'):
            # Matplotlib Axes instance or something that looks like it
            plot.set_title(title)
            plot.set_xlabel(xlabel)
            plot.set_ylabel(ylabel)
        else:
            # matplotlib.pyplot module
            plot.title(title)
            plot.xlabel(xlabel)
            plot.ylabel(ylabel)
    except Exception:
        # Not an MPL object or something that looks (enough) like it.
        # Don't crash on adding labels or title
        pass

