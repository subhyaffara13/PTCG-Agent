
def _enclose(object, alias=''): #FIXME: needs alias to hold returned object
    """create a function enclosure around the source of some object"""
    #XXX: dummy and stub should append a random string
    dummy = '__this_is_a_big_dummy_enclosing_function__'
    stub = '__this_is_a_stub_variable__'
    code = 'def %s():\n' % dummy
    code += indent(getsource(object, alias=stub, lstrip=True, force=True))
    code += indent('return %s\n' % stub)
    if alias: code += '%s = ' % alias
    code += '%s(); del %s\n' % (dummy, dummy)
   #code += "globals().pop('%s',lambda :None)()\n" % dummy
    return code

