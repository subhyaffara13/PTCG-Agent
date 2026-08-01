
def get_private(regionFDArrays, fd_index, ri, fd_map):
    region_fdArray = regionFDArrays[ri]
    region_fd_map = fd_map[fd_index]
    if ri in region_fd_map:
        region_fdIndex = region_fd_map[ri]
        private = region_fdArray[region_fdIndex].Private
    else:
        private = None
    return private

