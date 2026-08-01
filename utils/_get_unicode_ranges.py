
def _getUnicodeRanges():
    # build the ranges of codepoints for each unicode range bit, and cache result
    if not _unicodeStarts:
        unicodeRanges = [
            (start, (stop, bit))
            for bit, blocks in enumerate(OS2_UNICODE_RANGES)
            for _, (start, stop) in blocks
        ]
        for start, (stop, bit) in sorted(unicodeRanges):
            _unicodeStarts.append(start)
            _unicodeValues.append((stop, bit))
    return _unicodeStarts, _unicodeValues

