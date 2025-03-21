import inspect

import pyetr.utils


def get_line_no(item):
    if item:
        # Get the source file and line number
        _, start_line_number = inspect.getsourcelines(item)
        url_prefix = (
            "https://github.com/dreamingspires/PyETR/blob/master/pyetr/utils.py#L"
        )
        return f"\n[Link to code]({url_prefix}{start_line_number})\n\n"
    else:
        return ""


def main():
    out = []
    for name, func in vars(pyetr.utils).items():
        if name in pyetr.utils.__all__:
            doc = inspect.getdoc(func)
            if doc is not None:
                new_doc = doc
            else:
                new_doc = ""
            out.append(
                "`" + name + "`" + get_line_no(func) + "\n```\n" + new_doc + "\n```"
            )

    with open("./docs/reference/utils_index.md", "w+") as f:
        intro = "# Utilities Index\n\nBelow you'll find all of the utilities in pyetr.utils. You can use this page as an index of the available utilities.\n\n## "
        full_page = intro + "\n\n## ".join(out)
        f.write(full_page)
