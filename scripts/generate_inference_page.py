import inspect

import pyetr.inference

from .common import get_line_no


def main():
    out = []
    for name, func in vars(pyetr.inference).items():
        if name in pyetr.inference.__all__:
            doc = inspect.getdoc(func)
            if doc is not None:
                new_doc = doc
            else:
                new_doc = ""
            out.append(
                "`"
                + name
                + "`"
                + get_line_no(func, "inference")
                + "\n```\n"
                + new_doc
                + "\n```"
            )

    with open("./docs/reference/inference_index.md", "w+") as f:
        intro = "# Inference Index\n\nBelow you'll find all of the inference functions in pyetr.inference. You can use this page as an index of the inference methods.\n\n## "
        full_page = intro + "\n\n## ".join(out)
        f.write(full_page)
