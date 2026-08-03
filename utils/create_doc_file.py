import re

def create_doc_file(new_paper_name: str, public_classes: list[str]):
    """
    Create a new doc file to fill for the new model.

    Args:
        new_paper_name (`str`):
            The fully cased name (as in the official paper name) of the new model.
        public_classes (`list[str]`):
            A list of all the public classes that the model will have in the library.
    """
    added_note = (
        "\n\n⚠️ Note that this file is in Markdown but contain specific syntax for our doc-builder (similar to MDX) that "
        "may not be rendered properly in your Markdown viewer.\n\n-->\n\n"
    )
    copyright_for_markdown = re.sub(r"# ?", "", COPYRIGHT).replace("coding=utf-8\n", "<!--") + added_note

    doc_template = textwrap.dedent(
        f"""
        # {new_paper_name}

        ## Overview

        The {new_paper_name} model was proposed in [<INSERT PAPER NAME HERE>](<INSERT PAPER LINK HERE>) by <INSERT AUTHORS HERE>.
        <INSERT SHORT SUMMARY HERE>

        The abstract from the paper is the following:

        <INSERT PAPER ABSTRACT HERE>

        Tips:

        <INSERT TIPS ABOUT MODEL HERE>

        This model was contributed by [INSERT YOUR HF USERNAME HERE](https://huggingface.co/<INSERT YOUR HF USERNAME HERE>).
        The original code can be found [here](<INSERT LINK TO GITHUB REPO HERE>).

        ## Usage examples

        <INSERT SOME NICE EXAMPLES HERE>

        """
    )

    # Add public classes doc
    doc_for_classes = []
    for class_ in public_classes:
        doc = f"## {class_}\n\n[[autodoc]] {class_}"
        if "Model" in class_:
            doc += "\n    - forward"
        doc_for_classes.append(doc)

    class_doc = "\n\n".join(doc_for_classes)

    return copyright_for_markdown + doc_template + class_doc

