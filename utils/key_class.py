from typing import Dict, List, Tuple, Union

def key_class(updates, image_strip, image_rects: List[pg.Rect], is_white_key=True):
    """Return a keyboard key widget class

    Arguments:
    updates - a set into which a key instance adds itself if it needs
        redrawing.
    image_strip - The surface containing the images of all key states.
    image_rects - A list of Rects giving the regions within image_strip that
        are relevant to this key class.
    is_white_key (default True) - Set false if this is a black key.

    This function automates the creation of a key widget class for the
    three basic key types. A key has two basic states, up or down (
    depressed). Corresponding up and down images are drawn for each
    of these two states. But to give the illusion of depth, a key
    may have shadows cast upon it by the adjacent keys to its right.
    These shadows change depending on the up/down state of the key and
    its neighbors. So a key may support multiple images and states
    depending on the shadows. A key type is determined by the length
    of image_rects and the value of is_white.

    """

    # Naming convention: Variables used by the Key class as part of a
    # closure start with 'c_'.

    # State logic and shadows:
    #
    # A key may cast a shadow upon the key to its left. A black key casts a
    # shadow on an adjacent white key. The shadow changes depending of whether
    # the black or white key is depressed. A white key casts a shadow on the
    # white key to its left if it is up and the left key is down. Therefore
    # a keys state, and image it will draw, is determined entirely by its
    # itself and the key immediately adjacent to it on the right. A white key
    # is always assumed to have an adjacent white key.
    #
    # There can be up to eight key states, representing all permutations
    # of the three fundamental states of self up/down, adjacent white
    # right up/down, adjacent black up/down.
    #
    down_state_none = 0
    down_state_self = 1
    down_state_white = down_state_self << 1
    down_state_self_white = down_state_self | down_state_white
    down_state_black = down_state_white << 1
    down_state_self_black = down_state_self | down_state_black
    down_state_white_black = down_state_white | down_state_black
    down_state_all = down_state_self | down_state_white_black

    # Some values used in the class.
    #
    c_down_state_initial = down_state_none
    c_down_state_rect_initial = image_rects[0]
    c_updates = updates
    c_image_strip = image_strip
    c_width, c_height = image_rects[0].size

    # A key propagates its up/down state change to the adjacent white key on
    # the left by calling the adjacent key's _right_black_down or
    # _right_white_down method.
    #
    if is_white_key:
        key_color = "white"
    else:
        key_color = "black"
    c_notify_down_method = f"_right_{key_color}_down"
    c_notify_up_method = f"_right_{key_color}_up"

    # Images:
    #
    # A black key only needs two images, for the up and down states. Its
    # appearance is unaffected by the adjacent keys to its right, which cast no
    # shadows upon it.
    #
    # A white key with a no adjacent black to its right only needs three
    # images, for self up, self down, and both self and adjacent white down.
    #
    # A white key with both a black and white key to its right needs six
    # images: self up, self up and adjacent black down, self down, self and
    # adjacent white down, self and adjacent black down, and all three down.
    #
    # Each 'c_event' dictionary maps the current key state to a new key state,
    # along with corresponding image, for the related event. If no redrawing
    # is required for the state change then the image rect is simply None.
    #
    c_event_down: Dict[int, Tuple[int, pygame.Rect]] = {
        down_state_none: (down_state_self, image_rects[1])
    }
    c_event_up: Dict[int, Tuple[int, pygame.Rect]] = {
        down_state_self: (down_state_none, image_rects[0])
    }
    c_event_right_white_down: Dict[int, Tuple[int, Union[pygame.Rect, None]]] = {
        down_state_none: (down_state_none, None),
        down_state_self: (down_state_self, None),
    }
    c_event_right_white_up = c_event_right_white_down.copy()
    c_event_right_black_down = c_event_right_white_down.copy()
    c_event_right_black_up = c_event_right_white_down.copy()
    if len(image_rects) > 2:
        c_event_down[down_state_white] = (down_state_self_white, image_rects[2])
        c_event_up[down_state_self_white] = (down_state_white, image_rects[0])
        c_event_right_white_down[down_state_none] = (down_state_white, None)
        c_event_right_white_down[down_state_self] = (
            down_state_self_white,
            image_rects[2],
        )
        c_event_right_white_up[down_state_white] = (down_state_none, None)
        c_event_right_white_up[down_state_self_white] = (
            down_state_self,
            image_rects[1],
        )
        c_event_right_black_down[down_state_white] = (down_state_white, None)
        c_event_right_black_down[down_state_self_white] = (down_state_self_white, None)
        c_event_right_black_up[down_state_white] = (down_state_white, None)
        c_event_right_black_up[down_state_self_white] = (down_state_self_white, None)
    if len(image_rects) > 3:
        c_event_down[down_state_black] = (down_state_self_black, image_rects[4])
        c_event_down[down_state_white_black] = (down_state_all, image_rects[5])
        c_event_up[down_state_self_black] = (down_state_black, image_rects[3])
        c_event_up[down_state_all] = (down_state_white_black, image_rects[3])
        c_event_right_white_down[down_state_black] = (down_state_white_black, None)
        c_event_right_white_down[down_state_self_black] = (
            down_state_all,
            image_rects[5],
        )
        c_event_right_white_up[down_state_white_black] = (down_state_black, None)
        c_event_right_white_up[down_state_all] = (down_state_self_black, image_rects[4])
        c_event_right_black_down[down_state_none] = (down_state_black, image_rects[3])
        c_event_right_black_down[down_state_self] = (
            down_state_self_black,
            image_rects[4],
        )
        c_event_right_black_down[down_state_white] = (
            down_state_white_black,
            image_rects[3],
        )
        c_event_right_black_down[down_state_self_white] = (
            down_state_all,
            image_rects[5],
        )
        c_event_right_black_up[down_state_black] = (down_state_none, image_rects[0])
        c_event_right_black_up[down_state_self_black] = (
            down_state_self,
            image_rects[1],
        )
        c_event_right_black_up[down_state_white_black] = (
            down_state_white,
            image_rects[0],
        )
        c_event_right_black_up[down_state_all] = (down_state_self_white, image_rects[2])

    class OurKey(Key):
        key_data = KeyData(
            is_white_key,
            c_width,
            c_height,
            c_down_state_initial,
            c_down_state_rect_initial,
            c_notify_down_method,
            c_notify_up_method,
            c_updates,
            c_event_down,
            c_event_up,
            c_image_strip,
            c_event_right_white_down,
            c_event_right_white_up,
            c_event_right_black_down,
            c_event_right_black_up,
        )

    return OurKey

