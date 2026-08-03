import functools

def format_dateaxis(
    subplot, freq: BaseOffset, index: DatetimeIndex | PeriodIndex
) -> None:
    """
    Pretty-formats the date axis (x-axis).

    Major and minor ticks are automatically set for the frequency of the
    current underlying series.  As the dynamic mode is activated by
    default, changing the limits of the x axis will intelligently change
    the positions of the ticks.
    """
    import matplotlib.pyplot as plt

    # handle index specific formatting
    # Note: DatetimeIndex does not use this
    # interface. DatetimeIndex uses matplotlib.date directly
    if isinstance(index, ABCPeriodIndex):
        majlocator = TimeSeries_DateLocator(
            freq, dynamic_mode=True, minor_locator=False, plot_obj=subplot
        )
        minlocator = TimeSeries_DateLocator(
            freq, dynamic_mode=True, minor_locator=True, plot_obj=subplot
        )
        subplot.xaxis.set_major_locator(majlocator)
        subplot.xaxis.set_minor_locator(minlocator)

        majformatter = TimeSeries_DateFormatter(
            freq, dynamic_mode=True, minor_locator=False, plot_obj=subplot
        )
        minformatter = TimeSeries_DateFormatter(
            freq, dynamic_mode=True, minor_locator=True, plot_obj=subplot
        )
        subplot.xaxis.set_major_formatter(majformatter)
        subplot.xaxis.set_minor_formatter(minformatter)

        # x and y coord info
        subplot.format_coord = functools.partial(_format_coord, freq)

    elif isinstance(index, ABCTimedeltaIndex):
        subplot.xaxis.set_major_formatter(TimeSeries_TimedeltaFormatter(index.unit))
    else:
        raise TypeError("index type not supported")

    plt.draw_if_interactive()

