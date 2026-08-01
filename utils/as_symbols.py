
def as_symbols(symbols):
    """
    Return an iterable of LicenseSymbol objects from a ``symbols`` sequence of
    strings or LicenseSymbol-like objects.

    If an item is a string, then create a new LicenseSymbol for it using the
    string as key.
    If this is not a string it must be a LicenseSymbol- like type. Raise a
    TypeError expection if an item is neither a string or LicenseSymbol- like.
    """
    if symbols:
        for symbol in symbols:
            if not symbol:
                continue
            if isinstance(symbol, bytes):
                try:
                    symbol = str(symbol)
                except:
                    raise TypeError(f"{symbol!r} is not a string.")

            if isinstance(symbol, str):
                if symbol.strip():
                    yield LicenseSymbol(symbol)

            elif isinstance(symbol, LicenseSymbol):
                yield symbol

            elif LicenseSymbol.symbol_like(symbol):
                yield LicenseSymbolLike(symbol)

            else:
                raise TypeError(f"{symbol!r} is neither a string nor LicenseSymbol-like.")

