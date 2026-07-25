# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from classyscrapers.modules.control import addonPath, addonVersion, joinPath
from classyscrapers.windows.textviewer import TextViewerXML


def get(file):
	classyscrapers_path = addonPath()
	classyscrapers_version = addonVersion()
	helpFile = joinPath(classyscrapers_path, 'lib', 'classyscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]ClassyScrapers -  v%s - %s[/B]' % (classyscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', classyscrapers_path, heading=heading, text=text)
	windows.run()
	del windows