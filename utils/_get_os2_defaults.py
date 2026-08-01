
def _getOS2Defaults():
    return dict(
        version=3,
        xAvgCharWidth=0,
        usWeightClass=400,
        usWidthClass=5,
        fsType=0x0004,  # default: Preview & Print embedding
        ySubscriptXSize=0,
        ySubscriptYSize=0,
        ySubscriptXOffset=0,
        ySubscriptYOffset=0,
        ySuperscriptXSize=0,
        ySuperscriptYSize=0,
        ySuperscriptXOffset=0,
        ySuperscriptYOffset=0,
        yStrikeoutSize=0,
        yStrikeoutPosition=0,
        sFamilyClass=0,
        panose=Panose(),
        ulUnicodeRange1=0,
        ulUnicodeRange2=0,
        ulUnicodeRange3=0,
        ulUnicodeRange4=0,
        achVendID="????",
        fsSelection=0,
        usFirstCharIndex=0,
        usLastCharIndex=0,
        sTypoAscender=0,
        sTypoDescender=0,
        sTypoLineGap=0,
        usWinAscent=0,
        usWinDescent=0,
        ulCodePageRange1=0,
        ulCodePageRange2=0,
        sxHeight=0,
        sCapHeight=0,
        usDefaultChar=0,  # .notdef
        usBreakChar=32,  # space
        usMaxContext=0,
        usLowerOpticalPointSize=0,
        usUpperOpticalPointSize=0,
    )

