
def Object_remap_device_varidxes(self, varidxes_map):
    mapper = partial(_Device_mapVarIdx, mapping=varidxes_map, done=set())
    _visit(self, mapper)

