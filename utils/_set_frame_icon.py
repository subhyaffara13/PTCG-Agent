
def _set_frame_icon(frame):
    bundle = wx.IconBundle()
    for image in ('matplotlib.png', 'matplotlib_large.png'):
        icon = wx.Icon(_load_bitmap(image))
        if not icon.IsOk():
            return
        bundle.AddIcon(icon)
    frame.SetIcons(bundle)

