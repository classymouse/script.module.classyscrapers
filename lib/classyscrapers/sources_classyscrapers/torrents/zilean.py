# created by kodifitzwell
"""
    Classy Scrapers Project
"""

from json import loads as jsloads
import queue
from classyscrapers.modules import client
from classyscrapers.modules import source_utils
from classyscrapers.modules.torrent_base import TorrentSourceBase


class source(TorrentSourceBase):
    timeout = 5
    priority = 1
    pack_capable = True
    hasMovies = True
    hasEpisodes = True
    provider = 'zilean'
    min_seeders = 0
    _queue = queue.SimpleQueue()

    def __init__(self):
        self.language = ['en']
        self.base_link = 'https://zilean.stremio.ru'
        self.movieSearch_link = '/dmm/filtered?ImdbId=%s'
        self.tvSearch_link = '/dmm/filtered?ImdbId=%s&Season=%s&Episode=%s'

    def title_name_for_check(self, name):
        return name.replace('.(Archie.Bunker', '')

    def fetch_files(self, ctx):
        results = client.request(ctx['url'], timeout=self.timeout)
        # None / blank / non-list JSON = empty response, not a scraper crash
        if not results:
            return []
        try:
            parsed = jsloads(results)
        except Exception:
            return []
        return parsed if isinstance(parsed, list) else []

    def parse_file(self, file, ctx):
        hash_ = file.get('info_hash')
        raw = file.get('raw_title')
        if not hash_ or not raw:
            return None
        name = source_utils.clean_name(raw)
        try:
            dsize, isize = source_utils.convert_size(float(file['size']), to='GB')
        except Exception:
            dsize, isize = 0, None
        return {
            'hash': hash_,
            'name': name,
            'seeders': 0,
            'dsize': dsize,
            'isize': isize,
        }
