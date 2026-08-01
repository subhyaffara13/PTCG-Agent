
def hashlib(context):
    if isinstance(context.call_function_name_qual, str):
        qualname_list = context.call_function_name_qual.split(".")
        func = qualname_list[-1]

        if "hashlib" in qualname_list:
            return _hashlib_func(context, func)

        elif "crypt" in qualname_list and func in ("crypt", "mksalt"):
            return _crypt_crypt(context, func)

