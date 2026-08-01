
def mathml(expr, printer='content', **settings):
    """Returns the MathML representation of expr. If printer is presentation
    then prints Presentation MathML else prints content MathML.
    """
    if printer == 'presentation':
        return MathMLPresentationPrinter(settings).doprint(expr)
    else:
        return MathMLContentPrinter(settings).doprint(expr)

