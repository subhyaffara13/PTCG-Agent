
def rect_area_pts(rect):
    for l in range(rect.left, rect.right):
        for t in range(rect.top, rect.bottom):
            yield l, t

