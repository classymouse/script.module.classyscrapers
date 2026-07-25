# -*- coding: utf-8 -*-
"""
	Classy Scrapers — help text viewer
"""

from classyscrapers.modules.control import addonPath, addonVersion, joinPath, existsPath
from classyscrapers.windows.textviewer import TextViewerXML


def get(file):
	name = (file or '').strip()
	if not name:
		from classyscrapers.modules.control import notification
		return notification(message='Help file not specified')

	classyscrapers_path = addonPath()
	classyscrapers_version = addonVersion()
	helpFile = joinPath(classyscrapers_path, 'lib', 'classyscrapers', 'help', name + '.txt')
	if not existsPath(helpFile):
		from classyscrapers.modules.control import notification
		return notification(message='Help file missing: %s' % name)

	try:
		with open(helpFile, 'r', encoding='utf-8', errors='ignore') as r:
			text = r.read()
	except Exception as e:
		from classyscrapers.modules.control import notification
		return notification(message='Could not read help: %s' % e)

	heading = '[B]ClassyScrapers -  v%s - %s[/B]' % (classyscrapers_version, name)
	try:
		windows = TextViewerXML('textviewer.xml', classyscrapers_path, heading=heading, text=text)
		windows.run()
		del windows
	except Exception:
		# Settings-behind / skin failures — native viewer always works
		try:
			from xbmcgui import Dialog
			Dialog().textviewer(heading.replace('[B]', '').replace('[/B]', ''), text)
		except Exception as e:
			from classyscrapers.modules.control import notification
			notification(message='Help viewer failed: %s' % e)
