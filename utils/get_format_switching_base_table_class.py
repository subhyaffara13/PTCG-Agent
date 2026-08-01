
def getFormatSwitchingBaseTableClass(formatType):
    try:
        return formatSwitchingBaseTables[formatType]
    except KeyError:
        raise TypeError(f"Unsupported format type: {formatType!r}")

