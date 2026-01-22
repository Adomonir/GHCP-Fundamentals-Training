"""globex demo file

This file is part of the Globex Ltd codebase and will soon be migrated to Chroma Inc.
Its main purpose is to demonstrate bulk renaming operations.

"""
import logging
logger = logging.getLogger("chroma_demo")

"""Utility to perform bulk rename from 'globex' to 'chroma'.

Intentionally simplistic for demo purposes.
"""
import os, re, sys, pathlib

def case_preserving_replace(match):
    """Replace 'globex' with 'chroma' while preserving the case pattern."""
    original = match.group(0)
    if original.isupper():
        return 'CHROMA'
    elif original[0].isupper():
        return 'Chroma'
    else:
        return 'chroma'

def bulk_rename(root_path: str):
    pattern = re.compile(r'globex', re.IGNORECASE)
    for path in pathlib.Path(root_path).rglob('*.py'):
        text = path.read_text()
        replaced = pattern.sub(case_preserving_replace, text)
        if replaced != text:
            path.write_text(replaced)
            print(f"Updated {path}")

if __name__ == "__main__":
    bulk_rename(sys.argv[1] if len(sys.argv) > 1 else '.')
