
def get_adjustment() -> _TextAdjustment:
    use_east_asian_width = get_option("display.unicode.east_asian_width")
    if use_east_asian_width:
        return _EastAsianTextAdjustment()
    else:
        return _TextAdjustment()

