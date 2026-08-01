
def test_bxp_with_xlabels():
    def transform(stats):
        for s, label in zip(stats, list('ABCD')):
            s['label'] = label
        return stats

    _bxp_test_helper(transform_stats=transform)

