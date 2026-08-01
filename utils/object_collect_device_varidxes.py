
def Object_collect_device_varidxes(self, varidxes):
    adder = partial(_Device_recordVarIdx, s=varidxes)
    _visit(self, adder)

