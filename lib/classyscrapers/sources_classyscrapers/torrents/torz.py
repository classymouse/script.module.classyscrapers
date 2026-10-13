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
    priority = 1
    pack_capable = False
    hasMovies = True
    hasEpisodes = True
    provider = 'torz'
    min_seeders = 0

    def __init__(self):
        params = '/eyJzdG9yZXMiOlt7ImMiOiJwMnAiLCJ0IjoiIn1dfQ=='
        self.language = ['en']
        self.base_link = 'https://stremthru.elfhosted.com/stremio/torz'
        self.movieSearch_link = '%s/stream/movie/%%s.json' % params
        self.tvSearch_link = '%s/stream/series/%%s:%%s:%%s.json' % params

    def fetch_files(self, ctx):
        results = requests.get(ctx['url'], timeout=self.timeout)
        return (results.json() or {}).get('streams') or []

    def parse_file(self, file, ctx):
        _INFO = re.compile(r'(?:💾|📦).*')
        hash_ = file['infoHash']
        file_title = file['description'].splitlines()
        file_info = next((i for i in file_title if _INFO.search(i)), '')
        name = source_utils.clean_name(file_title[-1])
        package = None
        dsize = 0
        isize = None
        try:
            size = re.findall(
                r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))',
                file_info,
            )
            package = 'season' if ctx['episode_title'] is not None and len(size) > 1 else None
            dsize, isize = source_utils._size(size[0])
        except Exception:
            try:
                # keep parity with old scraper: string for display path, dsize stays 0
                _ = '%.2f GB' % (float(file['behaviorHints']['videoSize']) / 1073741824)
            except Exception:
                pass
            package = None
            dsize = 0
            isize = None
        return {
            'hash': hash_,
            'name': name,
            'seeders': 0,
            'dsize': dsize,
            'isize': isize,
            'package': package,
        }
