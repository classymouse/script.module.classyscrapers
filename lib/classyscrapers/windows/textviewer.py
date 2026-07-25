# -*- coding: utf-8 -*-
"""
	Classy Scrapers — text viewer window
"""

from classyscrapers.windows.base import BaseDialog


class TextViewerXML(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, *args)
		self.window_id = 2060
		self.heading = kwargs.get('heading') or ''
		self.text = kwargs.get('text') or ''

	def onInit(self):
		self.set_properties()
		try:
			self.setFocusId(self.window_id)
		except Exception:
			pass

	def run(self):
		self.doModal()

	def onAction(self, action):
		if action in self.closing_actions or action in self.selection_actions:
			self.close()

	def set_properties(self):
		self.setProperty('classyscrapers.text', self.text)
		self.setProperty('classyscrapers.heading', self.heading)
