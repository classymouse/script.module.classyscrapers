# created by kodifitzwell
"""
    Classy Scrapers Project
"""

import re
import requests
import queue
from classyscrapers.modules import source_utils
from classyscrapers.modules.torrent_base import TorrentSourceBase


class source(TorrentSourceBase):
    timeout = 7
    priority = 1
    pack_capable = True
    hasMovies = True
    hasEpisodes = True
    provider = 'torrentsdb'
    min_seeders = 0
    _queue = queue.SimpleQueue()
    _INFO = re.compile(r'(📅|👤).*')
    _SIZE = re.compile(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))')

    def __init__(self):
        self.language = ['en']
        self.base_link = 'https://torrentsdb.com'
        self.movieSearch_link = '/stream/movie/%s.json'
        self.tvSearch_link = '/stream/series/%s:%s:%s.json'
    # Currently supports YTS(+), EZTV(+), 1337x(+), TorrentCSV(+), 1lou(+), Nyaa(+), Sk-CzTorrent(+), 1TamilBlasters(+), LimeTorrent(+), 1TamilMV(+), RARBG(+), Knaben(+), ThePirateBay(+), KickassTorrents(+), AnimeTosho(+), ExtremlymTorrents(+), YggTorrent(+), TokyoTosho(+), Rutor(+), Rutracker(+), Torrent9(+), ilCorSaRoNeRo(+), Manual(+).

    def title_name_for_check(self, name):
        return name.replace('.(Archie.Bunker', '')

    def fetch_files(self, ctx):
        try:
            results = requests.get(ctx['url'], timeout=self.timeout)
            return (results.json() or {}).get('streams') or []
        except Exception:
            return []

    def parse_file(self, file, ctx):
        hash_ = file.get('infoHash')
        if not hash_:
            return None
        file_title = (file.get('title') or '').split('\n')
        if not file_title:
            return None
        try:
            file_info = [x for x in file_title if self._INFO.match(x)][0]
        except Exception:
            return None
        name = source_utils.clean_name(file_title[0])
        try:
            seeders = int(re.search(r'(\d+)', file_info).group(1))
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
