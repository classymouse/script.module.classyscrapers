# created by kodifitzwell
"""
    Classy Scrapers Project
"""

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
    provider = 'aiostreams'
    min_seeders = 0

    def __init__(self):
        self.language = ['en']
        self.base_link = 'https://aiostreamsfortheweebs.midnightignite.me'
        self.movieSearch_link = '/api/v1/search'
        self.tvSearch_link = '/api/v1/search'

    def _headers(self):
        return {'x-aiostreams-user-data': (
            'ewogICJwcmVzZXRzIjogWwogICAgewogICAgICAidHlwZSI6ICJ0b3JyZW50aW8iLAogICAgICAiaW5z'
            'dGFuY2VJZCI6ICJlN2IiLAogICAgICAiZW5hYmxlZCI6IGZhbHNlLAogICAgICAib3B0aW9ucyI6IHsK'
            'ICAgICAgICAibmFtZSI6ICJUb3JyZW50aW8iLAogICAgICAgICJ0aW1lb3V0IjogNjUwMCwKICAgICAg'
            'ICAicmVzb3VyY2VzIjogWwogICAgICAgICAgInN0cmVhbSIsCiAgICAgICAgICAiY2F0YWxvZyIsCiAg'
            'ICAgICAgICAibWV0YSIKICAgICAgICBdLAogICAgICAgICJwcm92aWRlcnMiOiBbXSwKICAgICAgICAi'
            'dXNlTXVsdGlwbGVJbnN0YW5jZXMiOiBmYWxzZQogICAgICB9CiAgICB9LAogICAgewogICAgICAidHlw'
            'ZSI6ICJjb21ldCIsCiAgICAgICJpbnN0YW5jZUlkIjogImY3YiIsCiAgICAgICJlbmFibGVkIjogdHJ1'
            'ZSwKICAgICAgIm9wdGlvbnMiOiB7CiAgICAgICAgIm5hbWUiOiAiQ29tZXQiLAogICAgICAgICJ0aW1l'
            'b3V0IjogNjUwMCwKICAgICAgICAicmVzb3VyY2VzIjogWwogICAgICAgICAgInN0cmVhbSIKICAgICAg'
            'ICBdLAogICAgICAgICJpbmNsdWRlUDJQIjogdHJ1ZSwKICAgICAgICAicmVtb3ZlVHJhc2giOiBmYWxz'
            'ZQogICAgICB9CiAgICB9LAogICAgewogICAgICAidHlwZSI6ICJtZWRpYWZ1c2lvbiIsCiAgICAgICJp'
            'bnN0YW5jZUlkIjogIjQ1MCIsCiAgICAgICJlbmFibGVkIjogdHJ1ZSwKICAgICAgIm9wdGlvbnMiOiB7'
            'CiAgICAgICAgIm5hbWUiOiAiTWVkaWFGdXNpb24iLAogICAgICAgICJ0aW1lb3V0IjogNjUwMCwKICAg'
            'ICAgICAicmVzb3VyY2VzIjogWwogICAgICAgICAgInN0cmVhbSIsCiAgICAgICAgICAiY2F0YWxvZyIs'
            'CiAgICAgICAgICAibWV0YSIKICAgICAgICBdLAogICAgICAgICJ1c2VDYWNoZWRSZXN1bHRzT25seSI6'
            'IHRydWUsCiAgICAgICAgImVuYWJsZVdhdGNobGlzdENhdGFsb2dzIjogZmFsc2UsCiAgICAgICAgImRv'
            'd25sb2FkVmlhQnJvd3NlciI6IGZhbHNlLAogICAgICAgICJjb250cmlidXRvclN0cmVhbXMiOiBmYWxz'
            'ZSwKICAgICAgICAiY2VydGlmaWNhdGlvbkxldmVsc0ZpbHRlciI6IFtdLAogICAgICAgICJudWRpdHlG'
            'aWx0ZXIiOiBbXQogICAgICB9CiAgICB9LAogICAgewogICAgICAidHlwZSI6ICJzdHJlbXRocnVUb3J6'
            'IiwKICAgICAgImluc3RhbmNlSWQiOiAiYWVkIiwKICAgICAgImVuYWJsZWQiOiB0cnVlLAogICAgICAi'
            'b3B0aW9ucyI6IHsKICAgICAgICAibmFtZSI6ICJTdHJlbVRocnUgVG9yeiIsCiAgICAgICAgInRpbWVv'
            'dXQiOiA2NTAwLAogICAgICAgICJyZXNvdXJjZXMiOiBbCiAgICAgICAgICAic3RyZWFtIgogICAgICAg'
            'IF0sCiAgICAgICAgImluY2x1ZGVQMlAiOiBmYWxzZSwKICAgICAgICAidXNlTXVsdGlwbGVJbnN0YW5j'
            'ZXMiOiBmYWxzZQogICAgICB9CiAgICB9LAogICAgewogICAgICAidHlwZSI6ICJ0b3JyZW50cy1kYiIs'
            'CiAgICAgICJpbnN0YW5jZUlkIjogImRkMiIsCiAgICAgICJlbmFibGVkIjogdHJ1ZSwKICAgICAgIm9w'
            'dGlvbnMiOiB7CiAgICAgICAgIm5hbWUiOiAiVG9ycmVudHNEQiIsCiAgICAgICAgInRpbWVvdXQiOiA2'
            'NTAwLAogICAgICAgICJyZXNvdXJjZXMiOiBbCiAgICAgICAgICAic3RyZWFtIiwKICAgICAgICAgICJj'
            'YXRhbG9nIiwKICAgICAgICAgICJtZXRhIgogICAgICAgIF0sCiAgICAgICAgInByb3ZpZGVycyI6IFsK'
            'ICAgICAgICAgICJ5dHMiLAogICAgICAgICAgIjEzMzd4IiwKICAgICAgICAgICJ0b3JyZW50Y3N2IiwK'
            'ICAgICAgICAgICIxbG91IiwKICAgICAgICAgICJueWFhIiwKICAgICAgICAgICJza3RvcnJlbnQiLAog'
            'ICAgICAgICAgIjF0YW1pbGJsYXN0ZXJzIiwKICAgICAgICAgICJsaW1ldG9ycmVudCIsCiAgICAgICAg'
            'ICAiMXRhbWlsbXYiLAogICAgICAgICAgInJhcmdiIiwKICAgICAgICAgICJrbmFiZW4iLAogICAgICAg'
            'ICAgInRoZXBpcmF0ZWJheSIsCiAgICAgICAgICAia2lja2Fzc3RvcnJlbnRzIiwKICAgICAgICAgICJh'
            'bmltZXRvc2hvIiwKICAgICAgICAgICJleHRyZW1seW10b3JyZW50cyIsCiAgICAgICAgICAieWdndG9y'
            'cmVudCIsCiAgICAgICAgICAidG9reW90b3NobyIsCiAgICAgICAgICAicnV0b3IiLAogICAgICAgICAg'
            'InJ1dHJhY2tlciIsCiAgICAgICAgICAidG9ycmVudDkiLAogICAgICAgICAgImlsY29yc2Fyb25lcm8i'
            'LAogICAgICAgICAgIm1hbnVhbCIKICAgICAgICBdLAogICAgICAgICJpbmNsdWRlUDJQIjogZmFsc2Us'
            'CiAgICAgICAgInVzZU11bHRpcGxlSW5zdGFuY2VzIjogZmFsc2UKICAgICAgfQogICAgfQogIF0sCiAg'
            'ImZvcm1hdHRlciI6IHsKICAgICJpZCI6ICJ0b3JyZW50aW8iLAogICAgImRlZmluaXRpb24iOiB7CiAg'
            'ICAgICJuYW1lIjogIiIsCiAgICAgICJkZXNjcmlwdGlvbiI6ICIiCiAgICB9CiAgfSwKICAic29ydENy'
            'aXRlcmlhIjogewogICAgImdsb2JhbCI6IFtdCiAgfQp9'
        )}

    def _context(self, data):
        # Search path has no %%s tokens; query goes in params instead.
        is_tv = 'tvshowtitle' in data
        title = data['tvshowtitle'] if is_tv else data['title']
        title = self._normalize_title(title)
        year = data['year']
        imdb = data['imdb']
        if is_tv:
            season = data['season']
            episode = data['episode']
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            episode_title = data['title']
            params = {'type': 'series', 'id': '%s:%s:%s' % (imdb, season, episode)}
        else:
            season = episode = None
            hdlr = year
            episode_title = None
            params = {'type': 'movie', 'id': '%s' % imdb}
        return {
            'data': data,
            'is_tv': is_tv,
            'title': title,
            'aliases': data.get('aliases') or [],
            'episode_title': episode_title,
            'year': year,
            'imdb': imdb,
            'season': season,
            'episode': episode,
            'hdlr': hdlr,
            'url': '%s%s' % (self.base_link, self.movieSearch_link),
            'params': params,
            'total_seasons': data.get('total_seasons') if is_tv else None,
        }

    def fetch_files(self, ctx):
        results = requests.get(
            ctx['url'], params=ctx.get('params'), headers=self._headers(), timeout=self.timeout
        )
        data = results.json() or {}
        return ((data.get('data') or {}).get('results')) or []

    def parse_file(self, file, ctx):
        hash_ = file.get('infoHash')
        if not hash_:
            return None
        raw = file.get('folderName') or file.get('filename') or ''
        file_title = raw.replace('┈➤', '\n').split('\n')
        if not file_title or not file_title[0]:
            return None
        name = source_utils.clean_name(file_title[0])
        try:
            seeders = int(file.get('seeders') or 0)
        except Exception:
            seeders = 0
        try:
            size = '%.2f GB' % (float(file['size']) / 1073741824)
            dsize, isize = source_utils._size(size)
        except Exception:
            dsize, isize = 0, None
        return {
            'hash': hash_,
            'name': name,
            'seeders': seeders,
            'dsize': dsize,
            'isize': isize,
        }
