
def test_textarea_properties():
    ta = TextArea('Foo')
    assert ta.get_text() == 'Foo'
    assert not ta.get_multilinebaseline()

    ta.set_text('Bar')
    ta.set_multilinebaseline(True)
    assert ta.get_text() == 'Bar'
    assert ta.get_multilinebaseline()

