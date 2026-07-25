# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from sys import argv
from urllib.parse import parse_qsl
from classyscrapers import sources_classyscrapers
from classyscrapers.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')

if action is None:
	control.openSettings('0.0', 'script.module.classyscrapers')

if action == "ClassyScrapersSettings":
	control.openSettings('0.0', 'script.module.classyscrapers')

elif action == 'ShowChangelog':
	from classyscrapers.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from classyscrapers.help import help
	help.get(params.get('name'))

elif action == "Defaults":
	control.setProviderDefaults()

elif action == "toggleAll":
	sourceList = []
	sourceList = sources_classyscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_classyscrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_classyscrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
	control.execute('RunPlugin(plugin://script.module.classyscrapers/?action=toggleAllTorrent&amp;setting=false)')
	control.sleep(500)
	sourceList = []
	from classyscrapers import pack_sources
	sourceList = pack_sources()
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == 'cleanSettings':
	control.clean_settings()

elif action == 'undesirablesSelect':
	from classyscrapers.modules.undesirables import undesirablesSelect
	undesirablesSelect()

elif action == 'undesirablesInput':
	from classyscrapers.modules.undesirables import undesirablesInput
	undesirablesInput()

elif action == 'undesirablesUserRemove':
	from classyscrapers.modules.undesirables import undesirablesUserRemove
	undesirablesUserRemove()

elif action == 'undesirablesUserRemoveAll':
	from classyscrapers.modules.undesirables import undesirablesUserRemoveAll
	undesirablesUserRemoveAll()

elif action == 'tools_clearLogFile':
	from classyscrapers.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='ClassyScrapers Log File Successfully Cleared')
	else: control.notification(message='Error clearing ClassyScrapers Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from classyscrapers.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_viewTorrentStats':
	from classyscrapers.modules import log_utils
	log_utils.view_TorrentStats(params.get('name'))

elif action == 'tools_uploadLogFile':
	from classyscrapers.modules import log_utils
	log_utils.upload_LogFile()

elif action == 'plexAuth':
	from classyscrapers.modules import plex
	plex.Plex().auth()

elif action == 'plexRevoke':
	from classyscrapers.modules import plex
	plex.Plex().revoke()

elif action == 'plexSelectShare':
	from classyscrapers.modules import plex
	plex.Plex().get_plexshare_resource()

elif action == 'plexSeeShare':
	from classyscrapers.modules import plex
	plex.Plex().see_active_shares()

elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))

elif action == 'TestProwlarrConnection':
	from classyscrapers.modules.prowlarr import Prowlarr
	prowlarr = Prowlarr()
	prowlarr.test()

elif action == 'ProwlarrIndexers':
	from classyscrapers.modules.prowlarr import Prowlarr
	prowlarr = Prowlarr()
	prowlarr.get_indexers()

elif action == 'mediafusionAuth':
	from classyscrapers.modules.mediafusion import MediaFusion
	mediafusion = MediaFusion()
	mediafusion.auth()

elif action == 'mediafusionReset':
	from classyscrapers.modules.mediafusion import MediaFusion
	mediafusion = MediaFusion()
	mediafusion.clear()

elif action == 'healthCheck':
	from classyscrapers.modules.health import Magneto
	Magneto().health_check()