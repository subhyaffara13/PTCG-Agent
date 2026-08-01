
def getStdCharSet(charset):
    # check to see if we can use a predefined charset value.
    predefinedCharSetVal = None
    predefinedCharSets = [
        (cffISOAdobeStringCount, cffISOAdobeStrings, 0),
        (cffExpertStringCount, cffIExpertStrings, 1),
        (cffExpertSubsetStringCount, cffExpertSubsetStrings, 2),
    ]
    lcs = len(charset)
    for cnt, pcs, csv in predefinedCharSets:
        if predefinedCharSetVal is not None:
            break
        if lcs > cnt:
            continue
        predefinedCharSetVal = csv
        for i in range(lcs):
            if charset[i] != pcs[i]:
                predefinedCharSetVal = None
                break
    return predefinedCharSetVal

