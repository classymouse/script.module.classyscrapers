# -*- coding: UTF-8 -*-

import os

sourcePath = os.path.dirname(__file__)
files = os.listdir(sourcePath)
# Skip __* and _* so helper modules (e.g. _base) are never treated as providers.
__all__ = [
    filename[:-3]
    for filename in files
    if filename.endswith('.py') and not filename.startswith('_')
]