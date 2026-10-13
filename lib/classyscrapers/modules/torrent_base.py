# -*- coding: utf-8 -*-
"""
Shared chassis for Classy torrent scrapers.

Subclasses supply host/URL templates + how to fetch/parse provider payloads.
This base owns title/hdlr/url setup, filters, quality, and the source dict shape.
"""

from classyscrapers.modules import source_utils


class TorrentSourceBase:
    timeout = 7
    priority = 1
    pack_capable = False
    # When True, single-ep miss may still accept season/show packs (Comet-style).
    pack_fallback = False
    hasMovies = True
    hasEpisodes = True
    language = ['en']
    min_seeders = 0
    provider = 'base'
    base_link = ''
    movieSearch_link = ''
    tvSearch_link = ''
    # Subclasses that are pack_capable set: _queue = queue.SimpleQueue()
    _queue = None

    def _normalize_title(self, title):
        return title.replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')

    def _context(self, data):
        """Build the shared scrape context (title, hdlr, url, ids)."""
        is_tv = 'tvshowtitle' in data
        title = data['tvshowtitle'] if is_tv else data['title']
        title = self._normalize_title(title)
        year = data['year']
        imdb = data['imdb']
        if is_tv:
            season = data['season']
            episode = data['episode']
            hdlr = 'S%02dE%02d' % (int(season), int(episode))
            url = '%s%s' % (self.base_link, self.tvSearch_link % (imdb, season, episode))
            episode_title = data['title']
        else:
            season = episode = None
            hdlr = year
            url = '%s%s' % (self.base_link, self.movieSearch_link % imdb)
            episode_title = None
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
            'url': url,
            'total_seasons': data.get('total_seasons') if is_tv else None,
        }

    def fetch_files(self, ctx):
        """Return a list of raw provider file objects. Override per scraper."""
        raise NotImplementedError

    def parse_file(self, file, ctx):
        """
        Map one raw file to a dict, or None to skip.
        Required keys: hash, name (cleaned release name).
        Optional: seeders, dsize, isize, package, last_season, episode_start, episode_end.
        """
        raise NotImplementedError

    def title_name_for_check(self, name):
        """Optional rename before check_title / pack filters (Archie.Bunker etc.)."""
        return name

    def _cache_pack_files(self, files):
        queue = getattr(self, '_queue', None)
        if not self.pack_capable or queue is None:
            return
        try:
            queue.put_nowait(files)  # seasons
            queue.put_nowait(files)  # shows
        except Exception:
            pass

    def accept_name(self, name, ctx):
        """
        Title gate after parse. Return False to skip, True to accept,
        or a dict of pack fields to merge into the source item.
        """
        check_name = self.title_name_for_check(name)
        if source_utils.check_title(ctx['title'], ctx['aliases'], check_name, ctx['hdlr'], ctx['year']):
            return True
        if not self.pack_fallback or ctx.get('total_seasons') is None:
            return False
        season = ctx.get('season')
        if season is None:
            return False
        valid, last_season = source_utils.filter_show_pack(
            ctx['title'], ctx['aliases'], ctx['imdb'], ctx['year'], season, check_name, ctx['total_seasons']
        )
        if valid:
            return {'package': 'show', 'last_season': last_season}
        valid, episode_start, episode_end = source_utils.filter_season_pack(
            ctx['title'], ctx['aliases'], ctx['year'], season, check_name
        )
        if valid:
            return {
                'package': 'season',
                'episode_start': episode_start,
                'episode_end': episode_end,
            }
        return False

    def accept_pack_name(self, name, ctx, search_series=False, total_seasons=None, bypass_filter=False):
        """Gate for sources_packs. Return pack meta dict or False."""
        check_name = self.title_name_for_check(name)
        season = ctx['season']
        episode_start = episode_end = 0
        last_season = None
        if not search_series:
            if not bypass_filter:
                valid, episode_start, episode_end = source_utils.filter_season_pack(
                    ctx['title'], ctx['aliases'], ctx['year'], season, check_name
                )
                if not valid:
                    return False
            return {
                'package': 'season',
                'episode_start': episode_start,
                'episode_end': episode_end,
            }
        if not bypass_filter:
            valid, last_season = source_utils.filter_show_pack(
                ctx['title'], ctx['aliases'], ctx['imdb'], ctx['year'], season, check_name, total_seasons
            )
            if not valid:
                return False
        else:
            last_season = total_seasons
        return {'package': 'show', 'last_season': last_season}

    def _build_item(self, parsed, ctx, name_info, pack_meta=None):
        hash_ = parsed['hash']
        name = parsed['name']
        seeders = int(parsed.get('seeders') or 0)
        magnet = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash_, name)
        quality, info = source_utils.get_release_quality(name_info, magnet)
        dsize = parsed.get('dsize')
        if dsize is None:
            dsize = 0
        isize = parsed.get('isize')
        if isize:
            info.insert(0, isize)
        info = ' | '.join(info)
        item = {
            'source': 'torrent',
            'language': 'en',
            'direct': False,
            'debridonly': True,
            'provider': self.provider,
            'url': magnet,
            'hash': hash_,
            'name': name,
            'name_info': name_info,
            'quality': quality,
            'info': info,
            'size': dsize,
            'seeders': seeders,
        }
        package = parsed.get('package')
        if isinstance(pack_meta, dict):
            # pack fields win over parse_file package when both set
            if pack_meta.get('package'):
                package = pack_meta['package']
            if pack_meta.get('last_season') is not None:
                item['last_season'] = pack_meta['last_season']
            if pack_meta.get('episode_start'):
                item['episode_start'] = pack_meta['episode_start']
                item['episode_end'] = pack_meta.get('episode_end')
        if package:
            item['package'] = package
        if parsed.get('last_season') is not None and 'last_season' not in item:
            item['last_season'] = parsed['last_season']
        if parsed.get('episode_start') and 'episode_start' not in item:
            item['episode_start'] = parsed['episode_start']
            item['episode_end'] = parsed.get('episode_end')
        return item

    def sources(self, data, hostDict):
        sources = []
        if not data:
            return sources
        append = sources.append
        provider = self.provider
        try:
            ctx = self._context(data)
            files = self.fetch_files(ctx) or []
            self._cache_pack_files(files)
            undesirables = source_utils.get_undesirables()
            check_foreign_audio = source_utils.check_foreign_audio()
        except Exception:
            source_utils.scraper_error(provider.upper())
            return sources

        for file in files:
            try:
                parsed = self.parse_file(file, ctx)
                if not parsed:
                    continue
                if not parsed.get('hash') or not parsed.get('name'):
                    continue

                pack_meta = self.accept_name(parsed['name'], ctx)
                if pack_meta is False or pack_meta is None:
                    continue

                name_info = source_utils.info_from_name(
                    parsed['name'], ctx['title'], ctx['year'], ctx['hdlr'], ctx['episode_title']
                )
                if source_utils.remove_lang(name_info, check_foreign_audio):
                    continue
                if undesirables and source_utils.remove_undesirables(name_info, undesirables):
                    continue

                seeders = int(parsed.get('seeders') or 0)
                if self.min_seeders > seeders:
                    continue

                append(self._build_item(parsed, ctx, name_info, pack_meta if isinstance(pack_meta, dict) else None))
            except Exception:
                source_utils.scraper_error(provider.upper())
        return sources

    def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
        sources = []
        if not data or not self.pack_capable:
            return sources
        append = sources.append
        provider = self.provider
        queue = getattr(self, '_queue', None)
        if queue is None:
            return sources
        try:
            ctx = self._context(data)
            files = queue.get(timeout=self.timeout + 1)
            undesirables = source_utils.get_undesirables()
            check_foreign_audio = source_utils.check_foreign_audio()
        except Exception:
            source_utils.scraper_error(provider.upper())
            return sources

        for file in files:
            try:
                parsed = self.parse_file(file, ctx)
                if not parsed:
                    continue
                if not parsed.get('hash') or not parsed.get('name'):
                    continue

                pack_meta = self.accept_pack_name(
                    parsed['name'], ctx,
                    search_series=search_series,
                    total_seasons=total_seasons,
                    bypass_filter=bypass_filter,
                )
                if not pack_meta:
                    continue

                name_info = source_utils.info_from_name(
                    parsed['name'], ctx['title'], ctx['year'],
                    season=ctx['season'], pack=pack_meta['package'],
                )
                if source_utils.remove_lang(name_info, check_foreign_audio):
                    continue
                if undesirables and source_utils.remove_undesirables(name_info, undesirables):
                    continue

                seeders = int(parsed.get('seeders') or 0)
                if self.min_seeders > seeders:
                    continue

                append(self._build_item(parsed, ctx, name_info, pack_meta))
            except Exception:
                source_utils.scraper_error(provider.upper())
        return sources
