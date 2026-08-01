
def test_load_from_url():
    path = Path(__file__).parent / "baseline_images/pngsuite/basn3p04.png"
    url = ('file:'
           + ('///' if sys.platform == 'win32' else '')
           + path.resolve().as_posix())
    with pytest.raises(ValueError, match="Please open the URL"):
        plt.imread(url)
    with urllib.request.urlopen(url) as file:
        plt.imread(file)

