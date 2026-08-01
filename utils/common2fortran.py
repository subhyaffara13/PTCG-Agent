
def common2fortran(common, tab=''):
    ret = ''
    for k in list(common.keys()):
        if k == '_BLNK_':
            ret = f"{ret}{tab}common {','.join(common[k])}"
        else:
            ret = f"{ret}{tab}common /{k}/ {','.join(common[k])}"
    return ret

