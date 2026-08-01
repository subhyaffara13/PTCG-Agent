
def test_operator_new_delete(capture):
    """Tests that class-specific operator new/delete functions are invoked"""

    class SubAliased(m.AliasedHasOpNewDelSize):
        pass

    with capture:
        a = m.HasOpNewDel()
        b = m.HasOpNewDelSize()
        d = m.HasOpNewDelBoth()
    assert (
        capture
        == """
        A new 8
        B new 4
        D new 32
    """
    )
    sz_alias = str(m.AliasedHasOpNewDelSize.size_alias)
    sz_noalias = str(m.AliasedHasOpNewDelSize.size_noalias)
    with capture:
        c = m.AliasedHasOpNewDelSize()
        c2 = SubAliased()
    assert capture == ("C new " + sz_noalias + "\n" + "C new " + sz_alias + "\n")

    with capture:
        del a
        pytest.gc_collect()
        del b
        pytest.gc_collect()
        del d
        pytest.gc_collect()
    assert (
        capture
        == """
        A delete
        B delete 4
        D delete
    """
    )

    with capture:
        del c
        pytest.gc_collect()
        del c2
        pytest.gc_collect()
    assert capture == ("C delete " + sz_noalias + "\n" + "C delete " + sz_alias + "\n")

