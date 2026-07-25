# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from classyscrapers.modules.control import addonPath, addonVersion, joinPath
from classyscrapers.windows.textviewer import TextViewerXML


def get():
	classyscrapers_path = addonPath()
	classyscrapers_version = addonVersion()
	changelogfile = joinPath(classyscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]ClassyScrapers -  v%s - ChangeLog[/B]' % classyscrapers_version
	windows = TextViewerXML('textviewer.xml', classyscrapers_path, heading=heading, text=text)
	windows.run()
	del windows