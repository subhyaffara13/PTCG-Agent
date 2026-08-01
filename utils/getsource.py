
def getsource(object, alias='', lstrip=False, enclosing=False, \
                                              force=False, builtin=False):
    """Return the text of the source code for an object. The source code for
    interactively-defined objects are extracted from the interpreter's history.

    The argument may be a module, class, method, function, traceback, frame,
    or code object.  The source code is returned as a single string.  An
    IOError is raised if the source code cannot be retrieved, while a
    TypeError is raised for objects where the source code is unavailable
    (e.g. builtins).

    If alias is provided, then add a line of code that renames the object.
    If lstrip=True, ensure there is no indentation in the first line of code.
    If enclosing=True, then also return any enclosing code.
    If force=True, catch (TypeError,IOError) and try to use import hooks.
    If builtin=True, force an import for any builtins
    """
    # hascode denotes a callable
    hascode = _hascode(object)
    # is a class instance type (and not in builtins)
    instance = _isinstance(object)

    # get source lines; if fail, try to 'force' an import
    try: # fails for builtins, and other assorted object types
        lines, lnum = getsourcelines(object, enclosing=enclosing)
    except (TypeError, IOError): # failed to get source, resort to import hooks
        if not force: # don't try to get types that findsource can't get
            raise
        if not getmodule(object): # get things like 'None' and '1'
            if not instance: return getimport(object, alias, builtin=builtin)
            # special handling (numpy arrays, ...)
            _import = getimport(object, builtin=builtin)
            name = getname(object, force=True)
            _alias = "%s = " % alias if alias else ""
            if alias == name: _alias = ""
            return _import+_alias+"%s\n" % name
        else: #FIXME: could use a good bit of cleanup, since using getimport...
            if not instance: return getimport(object, alias, builtin=builtin)
            # now we are dealing with an instance...
            name = object.__class__.__name__
            module = object.__module__
            if not name.isidentifier() or not all(i.isidentifier() for i in module.split('.')): #XXX: does exclusing malicious code exclude valid use?
                raise SyntaxError('invalid syntax')
            if module in ['builtins','__builtin__']:
                return getimport(object, alias, builtin=builtin)
            else: #FIXME: leverage getimport? use 'from module import name'?
                lines, lnum = ["%s = __import__('%s', fromlist=['%s']).%s\n" % (name,module,name,name)], 0
                obj = eval(lines[0].lstrip(name + ' = '))
                lines, lnum = getsourcelines(obj, enclosing=enclosing)

    # strip leading indent (helps ensure can be imported)
    if lstrip or alias:
        lines = _outdent(lines)

    # instantiate, if there's a nice repr  #XXX: BAD IDEA???
    if instance: #and force: #XXX: move into findsource or getsourcelines ?
        if '(' in repr(object): lines.append('%r\n' % object)
       #else: #XXX: better to somehow to leverage __reduce__ ?
       #    reconstructor,args = object.__reduce__()
       #    _ = reconstructor(*args)
        else: # fall back to serialization #XXX: bad idea?
            #XXX: better not duplicate work? #XXX: better new/enclose=True?
            lines = dumpsource(object, alias='', new=force, enclose=False)
            lines, lnum = [line+'\n' for line in lines.split('\n')][:-1], 0
       #else: object.__code__ # raise AttributeError

    # add an alias to the source code
    if alias:
        if hascode:
            skip = 0
            for line in lines: # skip lines that are decorators
                if not line.startswith('@'): break
                skip += 1
            #XXX: use regex from findsource / getsourcelines ?
            if lines[skip].lstrip().startswith('def '): # we have a function
                if alias != object.__name__:
                    lines.append('\n%s = %s\n' % (alias, object.__name__))
            elif 'lambda ' in lines[skip]: # we have a lambda
                if alias != lines[skip].split('=')[0].strip():
                    lines[skip] = '%s = %s' % (alias, lines[skip])
            else: # ...try to use the object's name
                if alias != object.__name__:
                    lines.append('\n%s = %s\n' % (alias, object.__name__))
        else: # class or class instance
            if instance:
                if alias != lines[-1].split('=')[0].strip():
                    lines[-1] = ('%s = ' % alias) + lines[-1]
            else:
                name = getname(object, force=True) or object.__name__
                if alias != name:
                    lines.append('\n%s = %s\n' % (alias, name))
    return ''.join(lines)

