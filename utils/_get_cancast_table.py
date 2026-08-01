
def _get_cancast_table():
    table = textwrap.dedent("""
        X ? b h i l q B H I L Q e f d g F D G S U V O M m
        ? # = = = = = = = = = = = = = = = = = = = = = . =
        b . # = = = = . . . . . = = = = = = = = = = = . =
        h . ~ # = = = . . . . . ~ = = = = = = = = = = . =
        i . ~ ~ # = = . . . . . ~ ~ = = ~ = = = = = = . =
        l . ~ ~ ~ # # . . . . . ~ ~ = = ~ = = = = = = . =
        q . ~ ~ ~ # # . . . . . ~ ~ = = ~ = = = = = = . =
        B . ~ = = = = # = = = = = = = = = = = = = = = . =
        H . ~ ~ = = = ~ # = = = ~ = = = = = = = = = = . =
        I . ~ ~ ~ = = ~ ~ # = = ~ ~ = = ~ = = = = = = . =
        L . ~ ~ ~ ~ ~ ~ ~ ~ # # ~ ~ = = ~ = = = = = = . ~
        Q . ~ ~ ~ ~ ~ ~ ~ ~ # # ~ ~ = = ~ = = = = = = . ~
        e . . . . . . . . . . . # = = = = = = = = = = . .
        f . . . . . . . . . . . ~ # = = = = = = = = = . .
        d . . . . . . . . . . . ~ ~ # = ~ = = = = = = . .
        g . . . . . . . . . . . ~ ~ ~ # ~ ~ = = = = = . .
        F . . . . . . . . . . . . . . . # = = = = = = . .
        D . . . . . . . . . . . . . . . ~ # = = = = = . .
        G . . . . . . . . . . . . . . . ~ ~ # = = = = . .
        S . . . . . . . . . . . . . . . . . . # = = = . .
        U . . . . . . . . . . . . . . . . . . . # = = . .
        V . . . . . . . . . . . . . . . . . . . . # = . .
        O . . . . . . . . . . . . . . . . . . . . = # . .
        M . . . . . . . . . . . . . . . . . . . . = = # .
        m . . . . . . . . . . . . . . . . . . . . = = . #
        """).strip().split("\n")
    dtypes = [type(np.dtype(c)) for c in table[0][2::2]]

    convert_cast = {".": Casting.unsafe, "~": Casting.same_kind,
                    "=": Casting.safe, "#": Casting.equiv,
                    " ": -1}

    cancast = {}
    for from_dt, row in zip(dtypes, table[1:]):
        cancast[from_dt] = {}
        for to_dt, c in zip(dtypes, row[2::2]):
            cancast[from_dt][to_dt] = convert_cast[c]
            # Of the types checked, numeric cast support same-value
            if from_dt in same_value_dtypes and to_dt in same_value_dtypes:
                cancast[from_dt][to_dt] |= Casting.same_value

    return cancast

