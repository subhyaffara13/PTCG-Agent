
def may_have_non_1to1(self):
    return False


def may_have_non_1to1(self):
    return True


def may_have_non_1to1(self):
    if self.Format == 1:
        return self.ExtSubTable.may_have_non_1to1()
    else:
        assert 0, "unknown format: %s" % self.Format


def may_have_non_1to1(self):
    return any(st.may_have_non_1to1() for st in self.SubTable if st)

