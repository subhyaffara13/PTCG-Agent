
def adjust_legend_subtitles(legend):
    """
    Make invisible-handle "subtitles" entries look more like titles.

    Note: This function is not part of the public API and may be changed or removed.

    """
    # Legend title not in rcParams until 3.0
    font_size = plt.rcParams.get("legend.title_fontsize", None)
    hpackers = legend.findobj(mpl.offsetbox.VPacker)[0].get_children()
    for hpack in hpackers:
        draw_area, text_area = hpack.get_children()
        handles = draw_area.get_children()
        if not all(artist.get_visible() for artist in handles):
            draw_area.set_width(0)
            for text in text_area.get_children():
                if font_size is not None:
                    text.set_size(font_size)

