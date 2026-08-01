
def maybe_color_bp(bp, color_tup, **kwds) -> None:
    # GH#30346, when users specifying those arguments explicitly, our defaults
    # for these four kwargs should be overridden; if not, use Pandas settings
    if not kwds.get("boxprops"):
        mpl.artist.setp(bp["boxes"], color=color_tup[0], alpha=1)
    if not kwds.get("whiskerprops"):
        mpl.artist.setp(bp["whiskers"], color=color_tup[1], alpha=1)
    if not kwds.get("medianprops"):
        mpl.artist.setp(bp["medians"], color=color_tup[2], alpha=1)
    if not kwds.get("capprops"):
        mpl.artist.setp(bp["caps"], color=color_tup[3], alpha=1)

