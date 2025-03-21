import pyetr.cases
from pyetr.cases import BaseExample

from .common import get_line_no


def main():
    out = []
    for name, case in vars(pyetr.cases).items():
        if (
            isinstance(case, type)
            and issubclass(case, BaseExample)
            and case != BaseExample
        ):
            out.append(name + get_line_no(case, "cases") + "\n```" + repr(case) + "```")

    with open("./docs/reference/case_index.md", "w+") as f:
        intro = "# Case Index\n\nBelow you'll find all of the cases in pyetr.cases, and their associated views. You can use this page as an index of the current cases.\n\n## "
        full_page = intro + "\n\n## ".join(out)
        f.write(full_page)
