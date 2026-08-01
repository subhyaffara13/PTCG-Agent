
def _test_text_features(fig):
    t = fig.text(1, 0.7, 'Default: fi ffi fl st',
                 fontsize=32, horizontalalignment='right')
    assert t.get_fontfeatures() is None
    t = fig.text(1, 0.4, 'Disabled: fi ffi fl st',
                 fontsize=32, horizontalalignment='right',
                 fontfeatures=['-liga'])
    assert t.get_fontfeatures() == ('-liga', )
    t = fig.text(1, 0.1, 'Discretionary: fi ffi fl st',
                 fontsize=32, horizontalalignment='right')
    t.set_fontfeatures(['dlig'])
    assert t.get_fontfeatures() == ('dlig', )

