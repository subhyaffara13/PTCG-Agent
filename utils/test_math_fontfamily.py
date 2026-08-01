
def test_math_fontfamily():
    fig = plt.figure(figsize=(10, 3))
    fig.text(0.2, 0.7, r"$This\ text\ should\ have\ one\ font$",
             size=24, math_fontfamily='dejavusans')
    fig.text(0.2, 0.3, r"$This\ text\ should\ have\ another$",
             size=24, math_fontfamily='stix')

