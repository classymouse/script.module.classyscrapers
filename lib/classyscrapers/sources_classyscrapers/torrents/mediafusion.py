# created by kodifitzwell
"""
    Classy Scrapers Project
"""

import re
import requests
from classyscrapers.modules import source_utils
from classyscrapers.modules.torrent_base import TorrentSourceBase


class source(TorrentSourceBase):
    timeout = 7
    priority = 2
    pack_capable = False  # packs parsed in sources via pack_fallback
    pack_fallback = True
    hasMovies = True
    hasEpisodes = True
    provider = 'mediafusion'
    min_seeders = 0
    # Upstream moved size/seeders from disk emoji to package emoji (and sometimes
    # only a bare size token). Match both so we do not drop every stream.
    _INFO = re.compile(
        r'(?:[💾📦].*|(?:(?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb)))'
    )
    _SIZE = re.compile(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))')
    _SEEDERS = re.compile(r'👤\s*(\d+)')

    def __init__(self):
        self.language = ['en']
        self.base_link = 'https://mediafusionfortheweebs.midnightignite.me'
        self.movieSearch_link = '/stream/movie/%s.json'
        self.tvSearch_link = '/stream/series/%s:%s:%s.json'

    def _headers(self):
        return {'encoded_user_data': (
            'eyJlbmFibGVfY2F0YWxvZ3MiOiBmYWxzZSwgIm1heF9zdHJlYW1zX3Blcl9yZXNvbHV0aW9uIjogOTks'
            'ICJ0b3JyZW50X3NvcnRpbmdfcHJpb3JpdHkiOiBbXSwgImNlcnRpZmljYXRpb25fZmlsdGVyIjogWyJE'
            'aXNhYmxlIl0sICJudWRpdHlfZmlsdGVyIjogWyJEaXNhYmxlIl19'
        )}

    def fetch_files(self, ctx):
        results = requests.get(ctx['url'], headers=self._headers(), timeout=self.timeout)
        return (results.json() or {}).get('streams') or []

    def parse_file(self, file, ctx):
        if 'url' in file:
            m = re.search(r'\b\w{40}\b', file.get('url') or '')
            if not m:
                return None
            hash_ = m.group()
        else:
            hash_ = file.get('infoHash')
            if not hash_:
                return None
        desc = file.get('description') or file.get('title') or ''
        desc_lines = desc.replace('┈➤', '\n').split('\n')
        info_matches = [x for x in desc_lines if self._INFO.search(x)]
        if not info_matches:
            return None
        file_info = info_matches[0]
        # Current MediaFusion puts tags in description line 0; the real
        # release name lives in behaviorHints.filename (Coco-style).
        hints = file.get('behaviorHints') or {}
        filename = (hints.get('filename') or '').strip()
        raw_name = filename or (desc_lines[0] if desc_lines else '')
        if not raw_name:
            return None
        name = source_utils.clean_name(raw_name)
        try:
            seeders = int(self._SEEDERS.search(file_info).group(1))
        except Exception:
            seeders = 0
        try:
            dsize, isize = source_utils._size(self._SIZE.findall(file_info)[-1])
        except Exception:
            dsize, isize = 0, None
        return {
            'hash': hash_,
            'name': name,
            'seeders': seeders,
            'dsize': dsize,
            'isize': isize,
        }
