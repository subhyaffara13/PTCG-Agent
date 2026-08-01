
def test_warn_deprecated():
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'foo was deprecated in Matplotlib 3\.10 and will be '
                            r'removed in 3\.12\.'):
        _api.warn_deprecated('3.10', name='foo')
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'The foo class was deprecated in Matplotlib 3\.10 and '
                            r'will be removed in 3\.12\.'):
        _api.warn_deprecated('3.10', name='foo', obj_type='class')
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'foo was deprecated in Matplotlib 3\.10 and will be '
                            r'removed in 3\.12\. Use bar instead\.'):
        _api.warn_deprecated('3.10', name='foo', alternative='bar')
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'foo was deprecated in Matplotlib 3\.10 and will be '
                            r'removed in 3\.12\. More information\.'):
        _api.warn_deprecated('3.10', name='foo', addendum='More information.')
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'foo was deprecated in Matplotlib 3\.10 and will be '
                            r'removed in 4\.0\.'):
        _api.warn_deprecated('3.10', name='foo', removal='4.0')
    with pytest.warns(mpl.MatplotlibDeprecationWarning,
                      match=r'foo was deprecated in Matplotlib 3\.10\.'):
        _api.warn_deprecated('3.10', name='foo', removal=False)
    with pytest.warns(PendingDeprecationWarning,
                      match=r'foo will be deprecated in a future version'):
        _api.warn_deprecated('3.10', name='foo', pending=True)
    with pytest.raises(ValueError, match=r'cannot have a scheduled removal'):
        _api.warn_deprecated('3.10', name='foo', pending=True, removal='3.12')
    with pytest.warns(mpl.MatplotlibDeprecationWarning, match=r'Complete replacement'):
        _api.warn_deprecated('3.10', message='Complete replacement', name='foo',
                             alternative='bar', addendum='More information.',
                             obj_type='class', removal='4.0')

