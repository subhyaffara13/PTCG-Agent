
def _load_bitmap(filename):
    """
    Load a wx.Bitmap from a file in the "images" directory of the Matplotlib
    data.
    """
    return wx.Bitmap(str(cbook._get_data_path('images', filename)))

