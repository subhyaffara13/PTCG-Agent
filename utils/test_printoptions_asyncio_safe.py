
def test_printoptions_asyncio_safe():
    asyncio = pytest.importorskip("asyncio")

    b = asyncio.Barrier(2)

    async def legacy_113():
        np.set_printoptions(legacy='1.13', precision=12)
        await b.wait()
        po = np.get_printoptions()
        assert po['legacy'] == '1.13'
        assert po['precision'] == 12
        orig_linewidth = po['linewidth']
        with np.printoptions(linewidth=34, legacy='1.21'):
            po = np.get_printoptions()
            assert po['legacy'] == '1.21'
            assert po['precision'] == 12
            assert po['linewidth'] == 34
        po = np.get_printoptions()
        assert po['linewidth'] == orig_linewidth
        assert po['legacy'] == '1.13'
        assert po['precision'] == 12

    async def legacy_125():
        np.set_printoptions(legacy='1.25', precision=7)
        await b.wait()
        po = np.get_printoptions()
        assert po['legacy'] == '1.25'
        assert po['precision'] == 7
        orig_linewidth = po['linewidth']
        with np.printoptions(linewidth=6, legacy='1.13'):
            po = np.get_printoptions()
            assert po['legacy'] == '1.13'
            assert po['precision'] == 7
            assert po['linewidth'] == 6
        po = np.get_printoptions()
        assert po['linewidth'] == orig_linewidth
        assert po['legacy'] == '1.25'
        assert po['precision'] == 7

    async def main():
        await asyncio.gather(legacy_125(), legacy_125())

    loop = asyncio.new_event_loop()
    asyncio.run(main())
    loop.close()

