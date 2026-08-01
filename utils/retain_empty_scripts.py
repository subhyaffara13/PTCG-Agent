
def retain_empty_scripts(self):
    # https://github.com/fonttools/fonttools/issues/518
    # https://bugzilla.mozilla.org/show_bug.cgi?id=1080739#c15
    return self.__class__ == ttLib.getTableClass("GSUB")

