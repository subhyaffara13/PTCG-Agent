
def test_ticket_742(xp):
    def SE(img, thresh=.7, size=4):
        mask = img > thresh
        rank = len(mask.shape)
        struct = ndimage.generate_binary_structure(rank, rank)
        struct = xp.asarray(struct)
        la, co = ndimage.label(mask,
                               struct)
        _ = ndimage.find_objects(la)

    if np.dtype(np.intp) != np.dtype('i'):
        shape = (3, 1240, 1240)
        a = np.random.rand(np.prod(shape)).reshape(shape)
        a = xp.asarray(a)
        # shouldn't crash
        SE(a)

