from typing import List

def HTMLBody(children: List[str], css_styles=css) -> str:
    """
    Generates the full html with css from a list of html spans

    Args:
        children (:obj:`List[str]`):
            A list of strings, assumed to be html elements

        css_styles (:obj:`str`, `optional`):
            Optional alternative implementation of the css

    Returns:
        :obj:`str`: An HTML string with style markup
    """
    children_text = "".join(children)
    return f"""
    <html>
        <head>
            <style>
                {css_styles}
            </style>
        </head>
        <body>
            <div class="tokenized-text" dir=auto>
            {children_text}
            </div>
        </body>
    </html>
    """

