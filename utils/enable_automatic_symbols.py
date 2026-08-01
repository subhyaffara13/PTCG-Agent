
def enable_automatic_symbols(shell):
    """Allow IPython to automatically create symbols (``isympy -a``). """
    # XXX: This should perhaps use tokenize, like int_to_Integer() above.
    # This would avoid re-executing the code, which can lead to subtle
    # issues.  For example:
    #
    # In [1]: a = 1
    #
    # In [2]: for i in range(10):
    #    ...:     a += 1
    #    ...:
    #
    # In [3]: a
    # Out[3]: 11
    #
    # In [4]: a = 1
    #
    # In [5]: for i in range(10):
    #    ...:     a += 1
    #    ...:     print b
    #    ...:
    # b
    # b
    # b
    # b
    # b
    # b
    # b
    # b
    # b
    # b
    #
    # In [6]: a
    # Out[6]: 12
    #
    # Note how the for loop is executed again because `b` was not defined, but `a`
    # was already incremented once, so the result is that it is incremented
    # multiple times.

    import re
    re_nameerror = re.compile(
        "name '(?P<symbol>[A-Za-z_][A-Za-z0-9_]*)' is not defined")

    def _handler(self, etype, value, tb, tb_offset=None):
        """Handle :exc:`NameError` exception and allow injection of missing symbols. """
        if etype is NameError and tb.tb_next and not tb.tb_next.tb_next:
            match = re_nameerror.match(str(value))

            if match is not None:
                # XXX: Make sure Symbol is in scope. Otherwise you'll get infinite recursion.
                self.run_cell("%(symbol)s = Symbol('%(symbol)s')" %
                              {'symbol': match.group("symbol")}, store_history=False)

                try:
                    code = self.user_ns['In'][-1]
                except (KeyError, IndexError):
                    pass
                else:
                    self.run_cell(code, store_history=False)
                    return None
                finally:
                    self.run_cell("del %s" % match.group("symbol"),
                                  store_history=False)

        stb = self.InteractiveTB.structured_traceback(
            etype, value, tb, tb_offset=tb_offset)
        self._showtraceback(etype, value, stb)

    shell.set_custom_exc((NameError,), _handler)

