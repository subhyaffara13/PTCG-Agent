
def locator_to_legend_entries(locator, limits, dtype):
    """Return levels and formatted levels for brief numeric legends."""
    raw_levels = locator.tick_values(*limits).astype(dtype)

    # The locator can return ticks outside the limits, clip them here
    raw_levels = [l for l in raw_levels if l >= limits[0] and l <= limits[1]]

    class dummy_axis:
        def get_view_interval(self):
            return limits

    if isinstance(locator, mpl.ticker.LogLocator):
        formatter = mpl.ticker.LogFormatter()
    else:
        formatter = mpl.ticker.ScalarFormatter()
        # Avoid having an offset/scientific notation which we don't currently
        # have any way of representing in the legend
        formatter.set_useOffset(False)
        formatter.set_scientific(False)
    formatter.axis = dummy_axis()

    formatted_levels = formatter.format_ticks(raw_levels)

    return raw_levels, formatted_levels

