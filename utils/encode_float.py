
def encodeFloat(f):
    # For CFF only, used in cffLib
    if f == 0.0:  # 0.0 == +0.0 == -0.0
        return realZeroBytes
    # Note: 14 decimal digits seems to be the limitation for CFF real numbers
    # in macOS. However, we use 8 here to match the implementation of AFDKO.
    s = "%.8G" % f
    if s[:2] == "0.":
        s = s[1:]
    elif s[:3] == "-0.":
        s = "-" + s[2:]
    elif s.endswith("000"):
        significantDigits = s.rstrip("0")
        s = "%sE%d" % (significantDigits, len(s) - len(significantDigits))
    else:
        dotIndex = s.find(".")
        eIndex = s.find("E")
        if dotIndex != -1 and eIndex != -1:
            integerPart = s[:dotIndex]
            fractionalPart = s[dotIndex + 1 : eIndex]
            exponent = int(s[eIndex + 1 :])
            newExponent = exponent - len(fractionalPart)
            if newExponent == 1:
                s = "%s%s0" % (integerPart, fractionalPart)
            else:
                s = "%s%sE%d" % (integerPart, fractionalPart, newExponent)
    if s.startswith((".0", "-.0")):
        sign, s = s.split(".", 1)
        s = "%s%sE-%d" % (sign, s.lstrip("0"), len(s))
    nibbles = []
    while s:
        c = s[0]
        s = s[1:]
        if c == "E":
            c2 = s[:1]
            if c2 == "-":
                s = s[1:]
                c = "E-"
            elif c2 == "+":
                s = s[1:]
            if s.startswith("0"):
                s = s[1:]
        nibbles.append(realNibblesDict[c])
    nibbles.append(0xF)
    if len(nibbles) % 2:
        nibbles.append(0xF)
    d = bytechr(30)
    for i in range(0, len(nibbles), 2):
        d = d + bytechr(nibbles[i] << 4 | nibbles[i + 1])
    return d

