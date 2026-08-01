
def test_on_offset_implementations(dt, offset):
    assume(not offset.normalize)
    # This case is flaky in CI 2024-11-04
    assume(
        not (
            WASM
            and isinstance(dt.tzinfo, zoneinfo.ZoneInfo)
            and dt.tzinfo.key == "Indian/Cocos"
            and isinstance(offset, pd.offsets.MonthBegin)
        )
    )
    # check that the class-specific implementations of is_on_offset match
    # the general case definition:
    #   (dt + offset) - offset == dt
    try:
        compare = (dt + offset) - offset
    except ValueError:
        # When dt + offset does not exist or is DST-ambiguous, assume(False) to
        # indicate to hypothesis that this is not a valid test case
        # DST-ambiguous example (GH41906):
        # dt = datetime.datetime(1900, 1, 1, tzinfo=ZoneInfo('Africa/Kinshasa'))
        # offset = MonthBegin(66)
        assume(False)

    assert offset.is_on_offset(dt) == (compare == dt)

