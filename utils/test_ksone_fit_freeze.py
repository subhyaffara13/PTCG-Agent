
def test_ksone_fit_freeze():
    # Regression test for ticket #1638.
    d = np.array(
        [-0.18879233, 0.15734249, 0.18695107, 0.27908787, -0.248649,
         -0.2171497, 0.12233512, 0.15126419, 0.03119282, 0.4365294,
         0.08930393, -0.23509903, 0.28231224, -0.09974875, -0.25196048,
         0.11102028, 0.1427649, 0.10176452, 0.18754054, 0.25826724,
         0.05988819, 0.0531668, 0.21906056, 0.32106729, 0.2117662,
         0.10886442, 0.09375789, 0.24583286, -0.22968366, -0.07842391,
         -0.31195432, -0.21271196, 0.1114243, -0.13293002, 0.01331725,
         -0.04330977, -0.09485776, -0.28434547, 0.22245721, -0.18518199,
         -0.10943985, -0.35243174, 0.06897665, -0.03553363, -0.0701746,
         -0.06037974, 0.37670779, -0.21684405])

    with np.errstate(invalid='ignore'):
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore",
                "The maximum number of subdivisions .50. has been achieved.",
                IntegrationWarning,
            )
            warnings.filterwarnings(
                "ignore",
                "floating point number truncated to an integer",
                RuntimeWarning,
            )
            stats.ksone.fit(d)

