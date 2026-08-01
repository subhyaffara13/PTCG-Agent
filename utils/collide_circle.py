
def collide_circle(left, right):
    """detect collision between two sprites using circles

    pygame.sprite.collide_circle(left, right): return bool

    Tests for collision between two sprites by testing whether two circles
    centered on the sprites overlap. If the sprites have a "radius" attribute,
    then that radius is used to create the circle; otherwise, a circle is
    created that is big enough to completely enclose the sprite's rect as
    given by the "rect" attribute. This function is intended to be passed as
    a collided callback function to the *collide functions. Sprites must have a
    "rect" and an optional "radius" attribute.

    New in pygame 1.8.0

    """

    xdistance = left.rect.centerx - right.rect.centerx
    ydistance = left.rect.centery - right.rect.centery
    distancesquared = xdistance**2 + ydistance**2

    try:
        leftradius = left.radius
    except AttributeError:
        leftrect = left.rect
        # approximating the radius of a square by using half of the diagonal,
        # might give false positives (especially if its a long small rect)
        leftradius = 0.5 * ((leftrect.width**2 + leftrect.height**2) ** 0.5)
        # store the radius on the sprite for next time
        left.radius = leftradius

    try:
        rightradius = right.radius
    except AttributeError:
        rightrect = right.rect
        # approximating the radius of a square by using half of the diagonal
        # might give false positives (especially if its a long small rect)
        rightradius = 0.5 * ((rightrect.width**2 + rightrect.height**2) ** 0.5)
        # store the radius on the sprite for next time
        right.radius = rightradius
    return distancesquared <= (leftradius + rightradius) ** 2

