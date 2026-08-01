
def calcCodePageRanges(unicodes):
    """Given a set of Unicode codepoints (integers), calculate the
    corresponding OS/2 CodePage range bits.
    This is a direct translation of FontForge implementation:
    https://github.com/fontforge/fontforge/blob/7b2c074/fontforge/tottf.c#L3158
    """
    bits = set()
    hasAscii = set(range(0x20, 0x7E)).issubset(unicodes)
    hasLineart = ord("┤") in unicodes

    for uni in unicodes:
        if uni == ord("Þ") and hasAscii:
            bits.add(0)  # Latin 1
        elif uni == ord("Ľ") and hasAscii:
            bits.add(1)  # Latin 2: Eastern Europe
            if hasLineart:
                bits.add(58)  # Latin 2
        elif uni == ord("Б"):
            bits.add(2)  # Cyrillic
            if ord("Ѕ") in unicodes and hasLineart:
                bits.add(57)  # IBM Cyrillic
            if ord("╜") in unicodes and hasLineart:
                bits.add(49)  # MS-DOS Russian
        elif uni == ord("Ά"):
            bits.add(3)  # Greek
            if hasLineart and ord("½") in unicodes:
                bits.add(48)  # IBM Greek
            if hasLineart and ord("√") in unicodes:
                bits.add(60)  # Greek, former 437 G
        elif uni == ord("İ") and hasAscii:
            bits.add(4)  # Turkish
            if hasLineart:
                bits.add(56)  # IBM turkish
        elif uni == ord("א"):
            bits.add(5)  # Hebrew
            if hasLineart and ord("√") in unicodes:
                bits.add(53)  # Hebrew
        elif uni == ord("ر"):
            bits.add(6)  # Arabic
            if ord("√") in unicodes:
                bits.add(51)  # Arabic
            if hasLineart:
                bits.add(61)  # Arabic; ASMO 708
        elif uni == ord("ŗ") and hasAscii:
            bits.add(7)  # Windows Baltic
            if hasLineart:
                bits.add(59)  # MS-DOS Baltic
        elif uni == ord("₫") and hasAscii:
            bits.add(8)  # Vietnamese
        elif uni == ord("ๅ"):
            bits.add(16)  # Thai
        elif uni == ord("エ"):
            bits.add(17)  # JIS/Japan
        elif uni == ord("ㄅ"):
            bits.add(18)  # Chinese: Simplified
        elif uni == ord("ㄱ"):
            bits.add(19)  # Korean wansung
        elif uni == ord("央"):
            bits.add(20)  # Chinese: Traditional
        elif uni == ord("곴"):
            bits.add(21)  # Korean Johab
        elif uni == ord("♥") and hasAscii:
            bits.add(30)  # OEM Character Set
        # TODO: Symbol bit has a special meaning (check the spec), we need
        # to confirm if this is wanted by default.
        # elif chr(0xF000) <= char <= chr(0xF0FF):
        #    codepageRanges.add(31)          # Symbol Character Set
        elif uni == ord("þ") and hasAscii and hasLineart:
            bits.add(54)  # MS-DOS Icelandic
        elif uni == ord("╚") and hasAscii:
            bits.add(62)  # WE/Latin 1
            bits.add(63)  # US
        elif hasAscii and hasLineart and ord("√") in unicodes:
            if uni == ord("Å"):
                bits.add(50)  # MS-DOS Nordic
            elif uni == ord("é"):
                bits.add(52)  # MS-DOS Canadian French
            elif uni == ord("õ"):
                bits.add(55)  # MS-DOS Portuguese

    if hasAscii and ord("‰") in unicodes and ord("∑") in unicodes:
        bits.add(29)  # Macintosh Character Set (US Roman)

    return bits

