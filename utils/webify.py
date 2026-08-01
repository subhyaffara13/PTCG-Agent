
def webify(color):
    if color.startswith('calc') or color.startswith('var'):
        return color
    else:
        # Check if the color can be shortened from 6 to 3 characters
        color = color.upper()
        if (len(color) == 6 and
            (    color[0] == color[1]
             and color[2] == color[3]
             and color[4] == color[5])):
            return f'#{color[0]}{color[2]}{color[4]}'
        else:
            return f'#{color}'

