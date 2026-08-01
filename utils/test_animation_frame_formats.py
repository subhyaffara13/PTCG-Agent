
def test_animation_frame_formats():
    # Animation frame_format should allow any of the following
    # if any of these are not allowed, an exception will be raised
    # test for gh issue #17908
    for fmt in ['png', 'jpeg', 'tiff', 'raw', 'rgba', 'ppm',
                'sgi', 'bmp', 'pbm', 'svg']:
        mpl.rcParams['animation.frame_format'] = fmt

