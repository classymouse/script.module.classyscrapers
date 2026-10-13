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
    provider = 'comet'
    min_seeders = 0
    _INFO = re.compile(r'💾.*')
    _SIZE = re.compile(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))')
    _SEEDERS = re.compile(r'👤\s*(\d+)')

    def __init__(self):
        params = (
            'eyJtYXhSZXN1bHRzUGVyUmVzb2x1dGlvbiI6MCwibWF4U2l6ZSI6MCwiY2FjaGVkT25seSI6ZmFsc2Us'
            'InJlbW92ZVRyYXNoIjp0cnVlLCJyZXN1bHRGb3JtYXQiOlsidGl0bGUiLCJtZXRhZGF0YSIsInNpemUi'
            'LCJsYW5ndWFnZXMiXSwiZGVicmlkU2VydmljZSI6InRvcnJlbnQiLCJkZWJyaWRBcGlLZXkiOiIiLCJk'
            'ZWJyaWRTdHJlYW1Qcm94eVBhc3N3b3JkIjoiIiwibGFuZ3VhZ2VzIjp7InJlcXVpcmVkIjpbXSwiZXhj'
            'bHVkZSI6W10sInByZWZlcnJlZCI6W119LCJyZXNvbHV0aW9ucyI6e30sIm9wdGlvbnMiOnsicmVtb3Zl'
            'X3JhbmtzX3VuZGVyIjotMTAwMDAwMDAwMDAsImFsbG93X2VuZ2xpc2hfaW5fbGFuZ3VhZ2VzIjpmYWxz'
            'ZSwicmVtb3ZlX3Vua25vd25fbGFuZ3VhZ2VzIjpmYWxzZX19'
        )
        self.language = ['en']
        self.base_link = 'https://cometfortheweebs.midnightignite.me'
        self.movieSearch_link = '/%s/stream/movie/%%s.json' % params
        self.tvSearch_link = '/%s/stream/series/%%s:%%s:%%s.json' % params

    def fetch_files(self, ctx):
        results = requests.get(ctx['url'], timeout=self.timeout)
        return (results.json() or {}).get('streams') or []

    def parse_file(self, file, ctx):
        if 'url' in file:
            m = re.search(r'\b\w{40}\b', file['url'] or '')
            if not m:
                return None
            hash_ = m.group()
        else:
            hash_ = file.get('infoHash')
            if not hash_:
                return None
        file_title = file['description'].replace('┈➤', '\n').split('\n')
        info_matches = [x for x in file_title if self._INFO.search(x)]
        if not info_matches:
            return None
        file_info = info_matches[0]
        name = source_utils.clean_name(file_title[0])
        try:
            seeders = int(self._SEEDERS.search(file_info).group(1))
        except Exception:
            seeders = 0
        try:
            dsize, isize = source_utils._size(self._SIZE.search(file_info).group(0))
        except Exception:
            dsize, isize = 0, None
        return {
            'hash': hash_,
            'name': name,
            'seeders': seeders,
            'dsize': dsize,
            'isize': isize,
        }
