
def _create_capsule(pointer, name, context, destructor):
    attr_found = False
    try:
        # based on https://github.com/python/cpython/blob/f4095e53ab708d95e019c909d5928502775ba68f/Objects/capsule.c#L209-L231
        uname = name.decode('utf8')
        for i in range(1, uname.count('.')+1):
            names = uname.rsplit('.', i)
            try:
                module = __import__(names[0])
            except ImportError:
                pass
            obj = module
            for attr in names[1:]:
                obj = getattr(obj, attr)
            capsule = obj
            attr_found = True
            break
    except Exception:
        pass

    if attr_found:
        if _PyCapsule_IsValid(capsule, name):
            return capsule
        raise UnpicklingError("%s object exists at %s but a PyCapsule object was expected." % (type(capsule), name))
    else:
        #warnings.warn('Creating a new PyCapsule %s for a C data structure that may not be present in memory. Segmentation faults or other memory errors are possible.' % (name,), UnpicklingWarning)
        capsule = _PyCapsule_New(pointer, name, destructor)
        _PyCapsule_SetContext(capsule, context)
        return capsule

