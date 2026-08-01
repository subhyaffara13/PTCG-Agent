
def set_default_weight_width_slant(font, location):
    if "OS/2" in font:
        if "wght" in location:
            weight_class = otRound(max(1, min(location["wght"], 1000)))
            if font["OS/2"].usWeightClass != weight_class:
                log.info("Setting OS/2.usWeightClass = %s", weight_class)
                font["OS/2"].usWeightClass = weight_class

        if "wdth" in location:
            # map 'wdth' axis (50..200) to OS/2.usWidthClass (1..9), rounding to closest
            widthValue = min(max(location["wdth"], 50), 200)
            widthClass = otRound(
                models.piecewiseLinearMap(widthValue, WDTH_VALUE_TO_OS2_WIDTH_CLASS)
            )
            if font["OS/2"].usWidthClass != widthClass:
                log.info("Setting OS/2.usWidthClass = %s", widthClass)
                font["OS/2"].usWidthClass = widthClass

    if "slnt" in location and "post" in font:
        italicAngle = max(-90, min(location["slnt"], 90))
        if font["post"].italicAngle != italicAngle:
            log.info("Setting post.italicAngle = %s", italicAngle)
            font["post"].italicAngle = italicAngle

