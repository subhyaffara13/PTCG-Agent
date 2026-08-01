
def test_mathtext_fallback_valid():
    for fallback in ['cm', 'stix', 'stixsans', 'None']:
        mpl.rcParams['mathtext.fallback'] = fallback

