
def test_orc_reader_decimal(dirpath):
    # Only testing the first 10 rows of data
    data = {
        "_col0": np.array(
            [
                Decimal("-1000.50000"),
                Decimal("-999.60000"),
                Decimal("-998.70000"),
                Decimal("-997.80000"),
                Decimal("-996.90000"),
                Decimal("-995.10000"),
                Decimal("-994.11000"),
                Decimal("-993.12000"),
                Decimal("-992.13000"),
                Decimal("-991.14000"),
            ],
            dtype="object",
        )
    }
    expected = pd.DataFrame.from_dict(data)

    inputfile = os.path.join(dirpath, "TestOrcFile.decimal.orc")
    got = read_orc(inputfile).iloc[:10]

    tm.assert_equal(expected, got)

