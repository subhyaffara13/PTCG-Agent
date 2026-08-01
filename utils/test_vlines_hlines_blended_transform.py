
def test_vlines_hlines_blended_transform():
    t = np.arange(5.0, 10.0, 0.1)
    s = np.exp(-t) + np.sin(2 * np.pi * t) + 10
    fig, (hax, vax) = plt.subplots(2, 1, figsize=(6, 6))
    hax.plot(t, s, '^')
    hax.hlines([10, 9], xmin=0, xmax=0.5,
               transform=hax.get_yaxis_transform(), colors='r')
    vax.plot(t, s, '^')
    vax.vlines([6, 7], ymin=0, ymax=0.15, transform=vax.get_xaxis_transform(),
               colors='r')

