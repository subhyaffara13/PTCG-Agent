
def test_to_excel_with_openpyxl_engine(tmp_excel):
    # GH 29854
    df1 = DataFrame({"A": np.linspace(1, 10, 10)})
    df2 = DataFrame({"B": np.linspace(1, 20, 10)})
    df = pd.concat([df1, df2], axis=1)
    styled = df.style.map(
        lambda val: f"color: {'red' if val < 0 else 'black'}"
    ).highlight_max()

    styled.to_excel(tmp_excel, engine="openpyxl")

