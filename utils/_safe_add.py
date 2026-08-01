
def _safe_add(df):
    # only add to the numeric items
    def is_ok(s):
        return (
            issubclass(s.dtype.type, (np.integer, np.floating)) and s.dtype != "uint8"
        )

    return DataFrame(dict((c, s + 1) if is_ok(s) else (c, s) for c, s in df.items()))

