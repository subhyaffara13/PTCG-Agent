
def validate_https___setuptools_pypa_io_en_latest_userguide_pyproject_config_html__definitions_ext_module(data, custom_formats={}, name_prefix=None):
    if not isinstance(data, (dict)):
        raise JsonSchemaValueException("" + (name_prefix or "data") + " must be object", value=data, name="" + (name_prefix or "data") + "", definition={'$id': '#/definitions/ext-module', 'title': 'Extension module', 'description': 'Parameters to construct a :class:`setuptools.Extension` object', 'type': 'object', 'required': ['name', 'sources'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'format': 'python-module-name-relaxed'}, 'sources': {'type': 'array', 'items': {'type': 'string'}}, 'include-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'define-macros': {'type': 'array', 'items': {'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}}, 'undef-macros': {'type': 'array', 'items': {'type': 'string'}}, 'library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'libraries': {'type': 'array', 'items': {'type': 'string'}}, 'runtime-library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'extra-objects': {'type': 'array', 'items': {'type': 'string'}}, 'extra-compile-args': {'type': 'array', 'items': {'type': 'string'}}, 'extra-link-args': {'type': 'array', 'items': {'type': 'string'}}, 'export-symbols': {'type': 'array', 'items': {'type': 'string'}}, 'swig-opts': {'type': 'array', 'items': {'type': 'string'}}, 'depends': {'type': 'array', 'items': {'type': 'string'}}, 'language': {'type': 'string'}, 'optional': {'type': 'boolean'}, 'py-limited-api': {'type': 'boolean'}}}, rule='type')
    data_is_dict = isinstance(data, dict)
    if data_is_dict:
        data__missing_keys = set(['name', 'sources']) - data.keys()
        if data__missing_keys:
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must contain " + (str(sorted(data__missing_keys)) + " properties"), value=data, name="" + (name_prefix or "data") + "", definition={'$id': '#/definitions/ext-module', 'title': 'Extension module', 'description': 'Parameters to construct a :class:`setuptools.Extension` object', 'type': 'object', 'required': ['name', 'sources'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'format': 'python-module-name-relaxed'}, 'sources': {'type': 'array', 'items': {'type': 'string'}}, 'include-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'define-macros': {'type': 'array', 'items': {'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}}, 'undef-macros': {'type': 'array', 'items': {'type': 'string'}}, 'library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'libraries': {'type': 'array', 'items': {'type': 'string'}}, 'runtime-library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'extra-objects': {'type': 'array', 'items': {'type': 'string'}}, 'extra-compile-args': {'type': 'array', 'items': {'type': 'string'}}, 'extra-link-args': {'type': 'array', 'items': {'type': 'string'}}, 'export-symbols': {'type': 'array', 'items': {'type': 'string'}}, 'swig-opts': {'type': 'array', 'items': {'type': 'string'}}, 'depends': {'type': 'array', 'items': {'type': 'string'}}, 'language': {'type': 'string'}, 'optional': {'type': 'boolean'}, 'py-limited-api': {'type': 'boolean'}}}, rule='required')
        data_keys = set(data.keys())
        if "name" in data_keys:
            data_keys.remove("name")
            data__name = data["name"]
            if not isinstance(data__name, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".name must be string", value=data__name, name="" + (name_prefix or "data") + ".name", definition={'type': 'string', 'format': 'python-module-name-relaxed'}, rule='type')
            if isinstance(data__name, str):
                if not custom_formats["python-module-name-relaxed"](data__name):
                    raise JsonSchemaValueException("" + (name_prefix or "data") + ".name must be python-module-name-relaxed", value=data__name, name="" + (name_prefix or "data") + ".name", definition={'type': 'string', 'format': 'python-module-name-relaxed'}, rule='format')
        if "sources" in data_keys:
            data_keys.remove("sources")
            data__sources = data["sources"]
            if not isinstance(data__sources, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".sources must be array", value=data__sources, name="" + (name_prefix or "data") + ".sources", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__sources_is_list = isinstance(data__sources, (list, tuple))
            if data__sources_is_list:
                data__sources_len = len(data__sources)
                for data__sources_x, data__sources_item in enumerate(data__sources):
                    if not isinstance(data__sources_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".sources[{data__sources_x}]".format(**locals()) + " must be string", value=data__sources_item, name="" + (name_prefix or "data") + ".sources[{data__sources_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "include-dirs" in data_keys:
            data_keys.remove("include-dirs")
            data__includedirs = data["include-dirs"]
            if not isinstance(data__includedirs, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".include-dirs must be array", value=data__includedirs, name="" + (name_prefix or "data") + ".include-dirs", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__includedirs_is_list = isinstance(data__includedirs, (list, tuple))
            if data__includedirs_is_list:
                data__includedirs_len = len(data__includedirs)
                for data__includedirs_x, data__includedirs_item in enumerate(data__includedirs):
                    if not isinstance(data__includedirs_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".include-dirs[{data__includedirs_x}]".format(**locals()) + " must be string", value=data__includedirs_item, name="" + (name_prefix or "data") + ".include-dirs[{data__includedirs_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "define-macros" in data_keys:
            data_keys.remove("define-macros")
            data__definemacros = data["define-macros"]
            if not isinstance(data__definemacros, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros must be array", value=data__definemacros, name="" + (name_prefix or "data") + ".define-macros", definition={'type': 'array', 'items': {'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}}, rule='type')
            data__definemacros_is_list = isinstance(data__definemacros, (list, tuple))
            if data__definemacros_is_list:
                data__definemacros_len = len(data__definemacros)
                for data__definemacros_x, data__definemacros_item in enumerate(data__definemacros):
                    if not isinstance(data__definemacros_item, (list, tuple)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}]".format(**locals()) + " must be array", value=data__definemacros_item, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}]".format(**locals()) + "", definition={'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}, rule='type')
                    data__definemacros_item_is_list = isinstance(data__definemacros_item, (list, tuple))
                    if data__definemacros_item_is_list:
                        data__definemacros_item_len = len(data__definemacros_item)
                        if data__definemacros_item_len > 0:
                            data__definemacros_item__0 = data__definemacros_item[0]
                            if not isinstance(data__definemacros_item__0, (str)):
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][0]".format(**locals()) + " must be string", value=data__definemacros_item__0, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][0]".format(**locals()) + "", definition={'description': 'macro name', 'type': 'string'}, rule='type')
                        if data__definemacros_item_len > 1:
                            data__definemacros_item__1 = data__definemacros_item[1]
                            data__definemacros_item__1_one_of_count10 = 0
                            if data__definemacros_item__1_one_of_count10 < 2:
                                try:
                                    if not isinstance(data__definemacros_item__1, (str)):
                                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + " must be string", value=data__definemacros_item__1, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
                                    data__definemacros_item__1_one_of_count10 += 1
                                except JsonSchemaValueException: pass
                            if data__definemacros_item__1_one_of_count10 < 2:
                                try:
                                    if not isinstance(data__definemacros_item__1, (NoneType)):
                                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + " must be null", value=data__definemacros_item__1, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + "", definition={'type': 'null'}, rule='type')
                                    data__definemacros_item__1_one_of_count10 += 1
                                except JsonSchemaValueException: pass
                            if data__definemacros_item__1_one_of_count10 != 1:
                                raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + " must be valid exactly by one definition" + (" (" + str(data__definemacros_item__1_one_of_count10) + " matches found)"), value=data__definemacros_item__1, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}][1]".format(**locals()) + "", definition={'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}, rule='oneOf')
                        if data__definemacros_item_len > 2:
                            raise JsonSchemaValueException("" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}]".format(**locals()) + " must contain only specified items", value=data__definemacros_item, name="" + (name_prefix or "data") + ".define-macros[{data__definemacros_x}]".format(**locals()) + "", definition={'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}, rule='items')
        if "undef-macros" in data_keys:
            data_keys.remove("undef-macros")
            data__undefmacros = data["undef-macros"]
            if not isinstance(data__undefmacros, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".undef-macros must be array", value=data__undefmacros, name="" + (name_prefix or "data") + ".undef-macros", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__undefmacros_is_list = isinstance(data__undefmacros, (list, tuple))
            if data__undefmacros_is_list:
                data__undefmacros_len = len(data__undefmacros)
                for data__undefmacros_x, data__undefmacros_item in enumerate(data__undefmacros):
                    if not isinstance(data__undefmacros_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".undef-macros[{data__undefmacros_x}]".format(**locals()) + " must be string", value=data__undefmacros_item, name="" + (name_prefix or "data") + ".undef-macros[{data__undefmacros_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "library-dirs" in data_keys:
            data_keys.remove("library-dirs")
            data__librarydirs = data["library-dirs"]
            if not isinstance(data__librarydirs, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".library-dirs must be array", value=data__librarydirs, name="" + (name_prefix or "data") + ".library-dirs", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__librarydirs_is_list = isinstance(data__librarydirs, (list, tuple))
            if data__librarydirs_is_list:
                data__librarydirs_len = len(data__librarydirs)
                for data__librarydirs_x, data__librarydirs_item in enumerate(data__librarydirs):
                    if not isinstance(data__librarydirs_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".library-dirs[{data__librarydirs_x}]".format(**locals()) + " must be string", value=data__librarydirs_item, name="" + (name_prefix or "data") + ".library-dirs[{data__librarydirs_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "libraries" in data_keys:
            data_keys.remove("libraries")
            data__libraries = data["libraries"]
            if not isinstance(data__libraries, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".libraries must be array", value=data__libraries, name="" + (name_prefix or "data") + ".libraries", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__libraries_is_list = isinstance(data__libraries, (list, tuple))
            if data__libraries_is_list:
                data__libraries_len = len(data__libraries)
                for data__libraries_x, data__libraries_item in enumerate(data__libraries):
                    if not isinstance(data__libraries_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".libraries[{data__libraries_x}]".format(**locals()) + " must be string", value=data__libraries_item, name="" + (name_prefix or "data") + ".libraries[{data__libraries_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "runtime-library-dirs" in data_keys:
            data_keys.remove("runtime-library-dirs")
            data__runtimelibrarydirs = data["runtime-library-dirs"]
            if not isinstance(data__runtimelibrarydirs, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".runtime-library-dirs must be array", value=data__runtimelibrarydirs, name="" + (name_prefix or "data") + ".runtime-library-dirs", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__runtimelibrarydirs_is_list = isinstance(data__runtimelibrarydirs, (list, tuple))
            if data__runtimelibrarydirs_is_list:
                data__runtimelibrarydirs_len = len(data__runtimelibrarydirs)
                for data__runtimelibrarydirs_x, data__runtimelibrarydirs_item in enumerate(data__runtimelibrarydirs):
                    if not isinstance(data__runtimelibrarydirs_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".runtime-library-dirs[{data__runtimelibrarydirs_x}]".format(**locals()) + " must be string", value=data__runtimelibrarydirs_item, name="" + (name_prefix or "data") + ".runtime-library-dirs[{data__runtimelibrarydirs_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "extra-objects" in data_keys:
            data_keys.remove("extra-objects")
            data__extraobjects = data["extra-objects"]
            if not isinstance(data__extraobjects, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-objects must be array", value=data__extraobjects, name="" + (name_prefix or "data") + ".extra-objects", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__extraobjects_is_list = isinstance(data__extraobjects, (list, tuple))
            if data__extraobjects_is_list:
                data__extraobjects_len = len(data__extraobjects)
                for data__extraobjects_x, data__extraobjects_item in enumerate(data__extraobjects):
                    if not isinstance(data__extraobjects_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-objects[{data__extraobjects_x}]".format(**locals()) + " must be string", value=data__extraobjects_item, name="" + (name_prefix or "data") + ".extra-objects[{data__extraobjects_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "extra-compile-args" in data_keys:
            data_keys.remove("extra-compile-args")
            data__extracompileargs = data["extra-compile-args"]
            if not isinstance(data__extracompileargs, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-compile-args must be array", value=data__extracompileargs, name="" + (name_prefix or "data") + ".extra-compile-args", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__extracompileargs_is_list = isinstance(data__extracompileargs, (list, tuple))
            if data__extracompileargs_is_list:
                data__extracompileargs_len = len(data__extracompileargs)
                for data__extracompileargs_x, data__extracompileargs_item in enumerate(data__extracompileargs):
                    if not isinstance(data__extracompileargs_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-compile-args[{data__extracompileargs_x}]".format(**locals()) + " must be string", value=data__extracompileargs_item, name="" + (name_prefix or "data") + ".extra-compile-args[{data__extracompileargs_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "extra-link-args" in data_keys:
            data_keys.remove("extra-link-args")
            data__extralinkargs = data["extra-link-args"]
            if not isinstance(data__extralinkargs, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-link-args must be array", value=data__extralinkargs, name="" + (name_prefix or "data") + ".extra-link-args", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__extralinkargs_is_list = isinstance(data__extralinkargs, (list, tuple))
            if data__extralinkargs_is_list:
                data__extralinkargs_len = len(data__extralinkargs)
                for data__extralinkargs_x, data__extralinkargs_item in enumerate(data__extralinkargs):
                    if not isinstance(data__extralinkargs_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".extra-link-args[{data__extralinkargs_x}]".format(**locals()) + " must be string", value=data__extralinkargs_item, name="" + (name_prefix or "data") + ".extra-link-args[{data__extralinkargs_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "export-symbols" in data_keys:
            data_keys.remove("export-symbols")
            data__exportsymbols = data["export-symbols"]
            if not isinstance(data__exportsymbols, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".export-symbols must be array", value=data__exportsymbols, name="" + (name_prefix or "data") + ".export-symbols", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__exportsymbols_is_list = isinstance(data__exportsymbols, (list, tuple))
            if data__exportsymbols_is_list:
                data__exportsymbols_len = len(data__exportsymbols)
                for data__exportsymbols_x, data__exportsymbols_item in enumerate(data__exportsymbols):
                    if not isinstance(data__exportsymbols_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".export-symbols[{data__exportsymbols_x}]".format(**locals()) + " must be string", value=data__exportsymbols_item, name="" + (name_prefix or "data") + ".export-symbols[{data__exportsymbols_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "swig-opts" in data_keys:
            data_keys.remove("swig-opts")
            data__swigopts = data["swig-opts"]
            if not isinstance(data__swigopts, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".swig-opts must be array", value=data__swigopts, name="" + (name_prefix or "data") + ".swig-opts", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__swigopts_is_list = isinstance(data__swigopts, (list, tuple))
            if data__swigopts_is_list:
                data__swigopts_len = len(data__swigopts)
                for data__swigopts_x, data__swigopts_item in enumerate(data__swigopts):
                    if not isinstance(data__swigopts_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".swig-opts[{data__swigopts_x}]".format(**locals()) + " must be string", value=data__swigopts_item, name="" + (name_prefix or "data") + ".swig-opts[{data__swigopts_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "depends" in data_keys:
            data_keys.remove("depends")
            data__depends = data["depends"]
            if not isinstance(data__depends, (list, tuple)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".depends must be array", value=data__depends, name="" + (name_prefix or "data") + ".depends", definition={'type': 'array', 'items': {'type': 'string'}}, rule='type')
            data__depends_is_list = isinstance(data__depends, (list, tuple))
            if data__depends_is_list:
                data__depends_len = len(data__depends)
                for data__depends_x, data__depends_item in enumerate(data__depends):
                    if not isinstance(data__depends_item, (str)):
                        raise JsonSchemaValueException("" + (name_prefix or "data") + ".depends[{data__depends_x}]".format(**locals()) + " must be string", value=data__depends_item, name="" + (name_prefix or "data") + ".depends[{data__depends_x}]".format(**locals()) + "", definition={'type': 'string'}, rule='type')
        if "language" in data_keys:
            data_keys.remove("language")
            data__language = data["language"]
            if not isinstance(data__language, (str)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".language must be string", value=data__language, name="" + (name_prefix or "data") + ".language", definition={'type': 'string'}, rule='type')
        if "optional" in data_keys:
            data_keys.remove("optional")
            data__optional = data["optional"]
            if not isinstance(data__optional, (bool)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".optional must be boolean", value=data__optional, name="" + (name_prefix or "data") + ".optional", definition={'type': 'boolean'}, rule='type')
        if "py-limited-api" in data_keys:
            data_keys.remove("py-limited-api")
            data__pylimitedapi = data["py-limited-api"]
            if not isinstance(data__pylimitedapi, (bool)):
                raise JsonSchemaValueException("" + (name_prefix or "data") + ".py-limited-api must be boolean", value=data__pylimitedapi, name="" + (name_prefix or "data") + ".py-limited-api", definition={'type': 'boolean'}, rule='type')
        if data_keys:
            raise JsonSchemaValueException("" + (name_prefix or "data") + " must not contain "+str(data_keys)+" properties", value=data, name="" + (name_prefix or "data") + "", definition={'$id': '#/definitions/ext-module', 'title': 'Extension module', 'description': 'Parameters to construct a :class:`setuptools.Extension` object', 'type': 'object', 'required': ['name', 'sources'], 'additionalProperties': False, 'properties': {'name': {'type': 'string', 'format': 'python-module-name-relaxed'}, 'sources': {'type': 'array', 'items': {'type': 'string'}}, 'include-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'define-macros': {'type': 'array', 'items': {'type': 'array', 'items': [{'description': 'macro name', 'type': 'string'}, {'description': 'macro value', 'oneOf': [{'type': 'string'}, {'type': 'null'}]}], 'additionalItems': False}}, 'undef-macros': {'type': 'array', 'items': {'type': 'string'}}, 'library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'libraries': {'type': 'array', 'items': {'type': 'string'}}, 'runtime-library-dirs': {'type': 'array', 'items': {'type': 'string'}}, 'extra-objects': {'type': 'array', 'items': {'type': 'string'}}, 'extra-compile-args': {'type': 'array', 'items': {'type': 'string'}}, 'extra-link-args': {'type': 'array', 'items': {'type': 'string'}}, 'export-symbols': {'type': 'array', 'items': {'type': 'string'}}, 'swig-opts': {'type': 'array', 'items': {'type': 'string'}}, 'depends': {'type': 'array', 'items': {'type': 'string'}}, 'language': {'type': 'string'}, 'optional': {'type': 'boolean'}, 'py-limited-api': {'type': 'boolean'}}}, rule='additionalProperties')
    return data

