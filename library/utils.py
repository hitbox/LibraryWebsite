import os
import re

def sitename_from_readme():
    """
    Return text after pound sign on first non-blank line, if found, otherwise None.
    """
    this_script_path = os.path.abspath(__file__)
    this_script_dir = os.path.dirname(this_script_path)
    readme_path = os.path.abspath(os.path.join(this_script_dir, '..', 'README.md'))
    with open(readme_path) as f:
        for line in f:
            if not line.strip():
                continue
            m = re.match('#(.*)$', line)
            return m.group(1).strip() if m else None

def splitcamel(s):
    """
    Split string s into CamelCase parts.
    """
    r = re.findall('[A-Z][^A-Z]+', s)
    if r:
        return r
    else:
        return [s]
