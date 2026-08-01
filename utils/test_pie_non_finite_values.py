
def test_pie_non_finite_values():
    fig, ax = plt.subplots()
    df = [5, float('nan'), float('inf')]

    with pytest.raises(ValueError, match='Wedge sizes must be finite numbers'):
        ax.pie(df, labels=['A', 'B', 'C'])

