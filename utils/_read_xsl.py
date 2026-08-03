from pathlib import Path


def _read_xsl(xsl):
    # Previously these values were allowed:
    if xsl == 'mathml/data/simple_mmlctop.xsl':
        xsl = 'simple_mmlctop.xsl'
    elif xsl == 'mathml/data/mmlctop.xsl':
        xsl = 'mmlctop.xsl'
    elif xsl == 'mathml/data/mmltex.xsl':
        xsl = 'mmltex.xsl'

    if xsl in ['simple_mmlctop.xsl', 'mmlctop.xsl', 'mmltex.xsl']:
        xslbytes = _read_binary('sympy.utilities.mathml.data', xsl)
    else:
        xslbytes = Path(xsl).read_bytes()

    return xslbytes

