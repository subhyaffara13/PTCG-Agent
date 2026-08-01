
def _test_complex_shaping(fig):
    # Raqm is Arabic for writing; note that because Arabic is RTL, the characters here
    # may seem to be in a different order than expected, but libraqm will order them
    # correctly for us.
    text = (
        'Arabic: \N{Arabic Letter REH}\N{Arabic FATHA}\N{Arabic Letter QAF}'
        '\N{Arabic SUKUN}\N{Arabic Letter MEEM}')
    math_signs = '\N{N-ary Product}\N{N-ary Coproduct}\N{N-ary summation}\N{Integral}'
    text = math_signs + text + math_signs
    fig.text(0.5, 0.75, text, size=32, ha='center', va='center')
    # Also check fallback behaviour:
    # - English should use cmr10
    # - Math signs should use DejaVu Sans Display (and thus be larger than the rest)
    # - Arabic should use DejaVu Sans
    fig.text(0.5, 0.25, text, size=32, ha='center', va='center',
             family=['cmr10', 'DejaVu Sans Display', 'DejaVu Sans'])

