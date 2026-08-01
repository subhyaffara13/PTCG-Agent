
def test_list_gui_frameworks():
    frameworks = backend_registry.list_gui_frameworks()
    assert not has_duplicates(frameworks)
    # Compare using sets as order is not important
    assert {*frameworks} == {
        "gtk3", "gtk4", "macosx", "qt", "qt5", "qt6", "tk", "wx",
    }

