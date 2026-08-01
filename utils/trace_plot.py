
def trace_plot(data, device=None, plot_segments=False, filter_freed=False):
    """Generate a visualization over time of the memory usage recorded by the trace as an html file.

    Args:
        data: Memory snapshot as generated from torch.cuda.memory._snapshot()
        device (torch.device, optional): Generate the trace for this device, needed if multiple devices have allocations.
        plot_segments (bool, optional): Plots memory returned from cudaMalloc, rather than individual allocations.
                                        Defaults to False.
        filter_freed (bool, optional): Filter out alloc-free paired events to only plot allocations that are not freed yet.
                                        Defaults to False to plot all trace events.

    Returns:
        str: HTML of visualization
    """
    if filter_freed:
        data = filter_alloc_free_pairs(data)

    return _format_viz(
        data,
        "Active Memory Timeline"
        if not plot_segments
        else "Active Cached Memory Timeline",
        device,
    )

