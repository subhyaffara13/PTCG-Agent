
def _impl_locale_comma():
    try:
        locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
    except locale.Error:
        print('SKIP: Locale de_DE.UTF-8 is not supported on this machine')
        return
    ticks = mticker.ScalarFormatter(useMathText=True, useLocale=True)
    fmt = '$\\mathdefault{%1.1f}$'
    x = ticks._format_maybe_minus_and_locale(fmt, 0.5)
    assert x == '$\\mathdefault{0{,}5}$'
    # Do not change , in the format string
    fmt = ',$\\mathdefault{,%1.1f},$'
    x = ticks._format_maybe_minus_and_locale(fmt, 0.5)
    assert x == ',$\\mathdefault{,0{,}5},$'
    # Make sure no brackets are added if not using math text
    ticks = mticker.ScalarFormatter(useMathText=False, useLocale=True)
    fmt = '%1.1f'
    x = ticks._format_maybe_minus_and_locale(fmt, 0.5)
    assert x == '0,5'

