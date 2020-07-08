# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

"""Script that is used to create the compatibility matrix in the documentation"""

import re
import eland
import pandas
import inspect


is_supported = []
supported_attr = re.compile(
    r"(?:[a-zA-Z0-9][a-zA-Z0-9_]*|__[a-zA-Z0-9][a-zA-Z0-9_]*__)"
)


def main():
    for prefix, pd_obj, ed_obj in [
        ("ed.DataFrame.", pandas.DataFrame, eland.DataFrame),
        ("ed.Series.", pandas.Series, eland.Series),
    ]:
        total = 0
        supported = 0
        for attr in sorted(dir(pd_obj), key=lambda x: (x.startswith("__"), x.lower())):
            val = getattr(pd_obj, attr)
            if inspect.isclass(val) or inspect.ismodule(val):
                continue

            total += 1
            suffix = ""
            if inspect.ismethod(val) or inspect.isfunction(val):
                suffix = "()"

            if supported_attr.fullmatch(attr):
                supported += hasattr(ed_obj, attr)
                is_supported.append((prefix + attr + suffix, hasattr(ed_obj, attr)))

        print(
            prefix.rstrip("."),
            f"{supported} / {total} ({100.0 * supported / total:.1f}%)",
        )

    column1_width = max([len(attr) + 1 for attr, _ in is_supported])
    row_delimiter = f"+{'-' * (column1_width + 5)}+------------+"

    print(row_delimiter)
    print(f"| Method or Property{' ' * (column1_width - 15)} | Supported? |")
    print(row_delimiter.replace("-", "="))

    for attr, supported in is_supported:
        print(
            f"| ``{attr}``{' ' * (column1_width - len(attr))}|{' **Yes**    ' if supported else ' No         '}|"
        )
        print(row_delimiter)


if __name__ == "__main__":
    main()
