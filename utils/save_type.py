
def save_type(pickler, obj, postproc_list=None):
    if obj in _typemap:
        logger.trace(pickler, "T1: %s", obj)
        # if obj in _incedental_types:
        #     warnings.warn('Type %r may only exist on this implementation of Python and cannot be unpickled in other implementations.' % (obj,), PicklingWarning)
        pickler.save_reduce(_load_type, (_typemap[obj],), obj=obj)
        logger.trace(pickler, "# T1")
    elif obj.__bases__ == (tuple,) and all([hasattr(obj, attr) for attr in ('_fields','_asdict','_make','_replace')]):
        # special case: namedtuples
        logger.trace(pickler, "T6: %s", obj)

        obj_name = getattr(obj, '__qualname__', getattr(obj, '__name__', None))
        if obj.__name__ != obj_name:
            if postproc_list is None:
                postproc_list = []
            postproc_list.append((setattr, (obj, '__qualname__', obj_name)))

        if not obj._field_defaults:
            _save_with_postproc(pickler, (_create_namedtuple, (obj.__name__, obj._fields, obj.__module__)), obj=obj, postproc_list=postproc_list)
        else:
            defaults = [obj._field_defaults[field] for field in obj._fields if field in obj._field_defaults]
            _save_with_postproc(pickler, (_create_namedtuple, (obj.__name__, obj._fields, obj.__module__, defaults)), obj=obj, postproc_list=postproc_list)
        logger.trace(pickler, "# T6")
        return

    # special caes: NoneType, NotImplementedType, EllipsisType, EnumMeta, etc
    elif obj is type(None):
        logger.trace(pickler, "T7: %s", obj)
        #XXX: pickler.save_reduce(type, (None,), obj=obj)
        pickler.write(GLOBAL + b'__builtin__\nNoneType\n')
        logger.trace(pickler, "# T7")
    elif obj is NotImplementedType:
        logger.trace(pickler, "T7: %s", obj)
        pickler.save_reduce(type, (NotImplemented,), obj=obj)
        logger.trace(pickler, "# T7")
    elif obj is EllipsisType:
        logger.trace(pickler, "T7: %s", obj)
        pickler.save_reduce(type, (Ellipsis,), obj=obj)
        logger.trace(pickler, "# T7")
    elif obj is EnumMeta:
        logger.trace(pickler, "T7: %s", obj)
        pickler.write(GLOBAL + b'enum\nEnumMeta\n')
        logger.trace(pickler, "# T7")
    elif obj is ExceptHookArgsType: #NOTE: must be after NoneType for pypy
        logger.trace(pickler, "T7: %s", obj)
        pickler.write(GLOBAL + b'threading\nExceptHookArgs\n')
        logger.trace(pickler, "# T7")

    else:
        _byref = getattr(pickler, '_byref', None)
        obj_recursive = id(obj) in getattr(pickler, '_postproc', ())
        incorrectly_named = not _locate_function(obj, pickler)
        if not _byref and not obj_recursive and incorrectly_named: # not a function, but the name was held over
            if postproc_list is None:
                postproc_list = []

            # thanks to Tom Stepleton pointing out pickler._session unneeded
            logger.trace(pickler, "T2: %s", obj)
            _dict, attrs = _get_typedict_type(obj, obj.__dict__.copy(), None, postproc_list) # copy dict proxy to a dict

           #print (_dict)
           #print ("%s\n%s" % (type(obj), obj.__name__))
           #print ("%s\n%s" % (obj.__bases__, obj.__dict__))
            slots = _dict.get('__slots__', ())
            if type(slots) == str:
                # __slots__ accepts a single string
                slots = (slots,)

            for name in slots:
                _dict.pop(name, None)

            if isinstance(obj, abc.ABCMeta):
                logger.trace(pickler, "ABC: %s", obj)
                _dict, attrs = _get_typedict_abc(obj, _dict, attrs, postproc_list)
                logger.trace(pickler, "# ABC")

            qualname = getattr(obj, '__qualname__', None)
            if attrs is not None:
                for k, v in attrs.items():
                    postproc_list.append((setattr, (obj, k, v)))
                # TODO: Consider using the state argument to save_reduce?
            if qualname is not None:
                postproc_list.append((setattr, (obj, '__qualname__', qualname)))

            if not hasattr(obj, '__orig_bases__'):
                _save_with_postproc(pickler, (_create_type, (
                    type(obj), obj.__name__, obj.__bases__, _dict
                )), obj=obj, postproc_list=postproc_list)
            else:
                # This case will always work, but might be overkill.
                _metadict = {
                    'metaclass': type(obj)
                }

                if _dict:
                    _dict_update = PartialType(_setitems, source=_dict)
                else:
                    _dict_update = None

                _save_with_postproc(pickler, (new_class, (
                    obj.__name__, obj.__orig_bases__, _metadict, _dict_update
                )), obj=obj, postproc_list=postproc_list)
            logger.trace(pickler, "# T2")
        else:
            obj_name = getattr(obj, '__qualname__', getattr(obj, '__name__', None))
            logger.trace(pickler, "T4: %s", obj)
            if incorrectly_named:
                warnings.warn(
                    "Cannot locate reference to %r." % (obj,),
                    PicklingWarning,
                    stacklevel=3,
                )
            if obj_recursive:
                warnings.warn(
                    "Cannot pickle %r: %s.%s has recursive self-references that "
                    "trigger a RecursionError." % (obj, obj.__module__, obj_name),
                    PicklingWarning,
                    stacklevel=3,
                )
           #print (obj.__dict__)
           #print ("%s\n%s" % (type(obj), obj.__name__))
           #print ("%s\n%s" % (obj.__bases__, obj.__dict__))
            StockPickler.save_global(pickler, obj, name=obj_name)
            logger.trace(pickler, "# T4")
    return

