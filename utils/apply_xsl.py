
def apply_xsl(mml, xsl):
    """Apply a xsl to a MathML string.

    Parameters
    ==========

    mml
        A string with MathML code.
    xsl
        A string giving the name of an xsl (xml stylesheet) file which can be
        found in sympy/utilities/mathml/data. The following files are supplied
        with SymPy:

        - mmlctop.xsl
        - mmltex.xsl
        - simple_mmlctop.xsl

        Alternatively, a full path to an xsl file can be given.

    Examples
    ========

    >>> from sympy.utilities.mathml import apply_xsl
    >>> xsl = 'simple_mmlctop.xsl'
    >>> mml = '<apply> <plus/> <ci>a</ci> <ci>b</ci> </apply>'
    >>> res = apply_xsl(mml,xsl)
    >>> print(res)
    <?xml version="1.0"?>
    <mrow xmlns="http://www.w3.org/1998/Math/MathML">
      <mi>a</mi>
      <mo> + </mo>
      <mi>b</mi>
    </mrow>
    """
    from lxml import etree

    parser = etree.XMLParser(resolve_entities=False)
    ac = etree.XSLTAccessControl.DENY_ALL

    s = etree.XML(_read_xsl(xsl), parser=parser)
    transform = etree.XSLT(s, access_control=ac)
    doc = etree.XML(mml, parser=parser)
    result = transform(doc)
    s = str(result)
    return s

