
def pyqt4_qtcore_transform():
    return AstroidBuilder(AstroidManager()).string_build(
        """

def SIGNAL(signal_name): pass

class QObject(object):
    def emit(self, signal): pass
"""
    )

