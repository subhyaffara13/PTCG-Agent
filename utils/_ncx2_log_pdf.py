
def _ncx2_log_pdf(x, df, nc):
    # We use (xs**2 + ns**2)/2 = (xs - ns)**2/2  + xs*ns, and include the
    # factor of exp(-xs*ns) into the ive function to improve numerical
    # stability at large values of xs. See also `rice.pdf`.
    df2 = df/2.0 - 1.0
    xs, ns = np.sqrt(x), np.sqrt(nc)
    res = sc.xlogy(df2/2.0, x/nc) - 0.5*(xs - ns)**2
    corr = sc.ive(df2, xs*ns) / 2.0
    # Return res + np.log(corr) avoiding np.log(0)
    return xpx.apply_where(
        corr > 0,
        (res, corr),
        lambda r, c: r + np.log(c),
        fill_value=-np.inf)

