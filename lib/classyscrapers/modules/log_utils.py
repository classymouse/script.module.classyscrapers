# -*- coding: utf-8 -*-
"""
	Classy Scrapers Module - logging helpers.

	File logs stay short and readable (Shield / Android): no Kodi COLOR markup,
	no full HTTP payloads, no reverse-rewrite of the whole file on every line.
"""

from datetime import datetime
import inspect
import re
from classyscrapers.modules.control import transPath, setting as getSetting, lang, joinPath, existsPath

LOGDEBUG = 0
LOGINFO = 1
LOGWARNING = 2
LOGERROR = 3
LOGFATAL = 4
LOGNONE = 5  # not used

debug_list = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'FATAL']
# Plain prefix for file + xbmc.log - COLOR tags are useless in both.
DEBUGPREFIX = '[ClassyScrapers %s]'
LOGPATH = transPath('special://logpath/')
LOG_FILENAME = 'classyscrapers.log'
OLD_LOG_FILENAME = 'classyscrapers.old.log'

# Cap single messages so one bad scraper can't inflate the log by megabytes.
_MAX_MSG_CHARS = 1200
_COLOR_RE = re.compile(r'\[/?COLOR[^\]]*\]', re.I)
_BOLD_RE = re.compile(r'\[/?B\]', re.I)
_CTRL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')


def _strip_markup(text):
	text = _COLOR_RE.sub('', str(text or ''))
	return _BOLD_RE.sub('', text)


def rotate_session_log():
	'''
	On service start: classyscrapers.log → classyscrapers.old.log (same as Crew/Classy).
	Keeps one previous session; empty files are left alone.
	'''
	try:
		import xbmcvfs
		log_path = joinPath(LOGPATH, LOG_FILENAME)
		old_path = joinPath(LOGPATH, OLD_LOG_FILENAME)
		if not existsPath(log_path):
			return
		try:
			if xbmcvfs.Stat(log_path).st_size() <= 0:
				return
		except Exception:
			pass
		if existsPath(old_path):
			try:
				xbmcvfs.delete(old_path)
			except Exception:
				pass
		try:
			xbmcvfs.rename(log_path, old_path)
		except Exception:
			pass
	except Exception:
		pass


def _safe_text(msg):
	'''Coerce to str; strip Kodi markup / NULs. Keep newlines for tracebacks.'''
	if isinstance(msg, int):
		msg = lang(msg)
	if isinstance(msg, bytes):
		msg = msg.decode('utf-8', errors='replace')
	else:
		msg = str(msg)
	msg = _strip_markup(msg)
	# Old isprintable() treated "\n" as non-printable and forced NORMALIZE on every traceback.
	if _CTRL_RE.search(msg):
		msg = _CTRL_RE.sub('', msg)
		try:
			msg = normalize(msg)
		except Exception:
			pass
	if len(msg) > _MAX_MSG_CHARS:
		omitted = len(msg) - _MAX_MSG_CHARS
		msg = '%s … [truncated %d chars]' % (msg[:_MAX_MSG_CHARS], omitted)
	return msg


def _format_line(level, msg):
	stamp = '%s %s' % (datetime.now().date(), str(datetime.now().time())[:8])
	tag = DEBUGPREFIX % debug_list[level]
	# Keep multi-line messages indented under the header for readability.
	body = msg.replace('\r\n', '\n').replace('\r', '\n')
	if '\n' in body:
		parts = body.split('\n')
		body = parts[0] + '\n' + '\n'.join('  ' + p for p in parts[1:] if p != '')
	return '[%s] %s: %s' % (stamp, tag, body)


def log(msg, caller=None, level=LOGINFO):
	debug_enabled = getSetting('debug.enabled') == 'true'
	if not debug_enabled:
		return
	debug_location = getSetting('debug.location')

	try:
		msg = _safe_text(msg)

		if caller == 'scraper_error':
			pass
		elif caller is not None and level != LOGERROR:
			func = inspect.currentframe().f_back.f_code
			line_number = inspect.currentframe().f_back.f_lineno
			caller = '%s.%s()' % (caller, func.co_name)
			msg = 'From %s L%s: %s' % (caller, line_number, msg)
		elif caller is not None and level == LOGERROR:
			msg = 'From %s.%s() L%s: %s' % (caller[0], caller[1], caller[2], msg)

		if debug_location == '1':
			log_file = joinPath(LOGPATH, 'classyscrapers.log')
			line = _format_line(level, msg)
			# Always append. Reverse-rewrite re-reads the whole file per line and
			# balloons I/O on Shield/Android - ignore debug.reversed for writes.
			try:
				with open(log_file, 'a', encoding='utf-8') as f:
					f.write(line.rstrip('\r\n') + '\n')
			except FileNotFoundError:
				with open(log_file, 'w', encoding='utf-8') as f:
					f.write(line.rstrip('\r\n') + '\n')
		else:
			import xbmc
			xbmc.log('%s: %s' % (DEBUGPREFIX % debug_list[level], msg), level)
	except Exception as e:
		import traceback
		traceback.print_exc()
		import xbmc
		xbmc.log('[ script.module.classyscrapers ] log_utils.log() Logging Failure: %s' % (e), LOGERROR)


def error(message=None, exception=True):
	try:
		import sys
		if exception:
			type, value, traceback = sys.exc_info()
			addon = 'script.module.classyscrapers'
			filename = (traceback.tb_frame.f_code.co_filename)
			filename = filename.split(addon)[1]
			name = traceback.tb_frame.f_code.co_name
			linenumber = traceback.tb_lineno
			errortype = type.__name__
			errormessage = value or getattr(value, 'message', None)
			if str(errormessage) == '':
				return
			if message:
				message += ' -> '
			else:
				message = ''
			message += str(errortype) + ' -> ' + str(errormessage)
			caller = [filename, name, linenumber]
		else:
			caller = None
		del (type, value, traceback)  # So we don't leave our local labels/objects dangling
		log(msg=message, caller=caller, level=LOGERROR)
	except Exception as e:
		import xbmc
		xbmc.log('[ script.module.classyscrapers ] log_utils.error() Logging Failure: %s' % (e), LOGERROR)


def clear_logFile():
	cleared = False
	try:
		from classyscrapers.modules.control import yesnoDialog
		if not yesnoDialog(lang(32060), '', ''):
			return 'canceled'
		log_file = joinPath(LOGPATH, 'classyscrapers.log')
		if not existsPath(log_file):
			f = open(log_file, 'w', encoding='utf-8')
			return f.close()
		f = open(log_file, 'r+', encoding='utf-8')
		f.truncate(0)  # need '0' when using r
		f.close()
		cleared = True
	except Exception as e:
		import xbmc
		xbmc.log('[ script.module.classyscrapers ] log_utils.clear_logFile() Failure: %s' % (e), LOGERROR)
		cleared = False
	return cleared


def view_LogFile(name):
	try:
		from classyscrapers.windows.textviewer import TextViewerXML
		from classyscrapers.modules.control import addonPath
		log_file = joinPath(LOGPATH, '%s.log' % name.lower())
		if not existsPath(log_file):
			from classyscrapers.modules.control import notification
			return notification(message='Log File not found, likely logging is not enabled.')
		f = open(log_file, 'r', encoding='utf-8', errors='ignore')
		text = f.read()
		f.close()
		heading = '[B]%s -  LogFile[/B]' % name
		windows = TextViewerXML('textviewer.xml', addonPath(), heading=heading, text=text)
		windows.run()
		del windows
	except Exception:
		error()


def view_TorrentStats(name):
	try:
		from classyscrapers.windows.textviewer import TextViewerXML
		from classyscrapers.modules.control import addonPath
		log_file = joinPath(LOGPATH, '%s.log' % name.lower())
		if not existsPath(log_file):
			from classyscrapers.modules.control import notification
			return notification(message='Log File not found, likely logging is not enabled.')
		f = open(log_file, 'r', encoding='utf-8', errors='ignore')
		text = f.read()
		f.close()
		stats_lines = '\n'.join([line for line in text.splitlines() if '#STATS' in line])
		heading = '[B]%s -  LogFile[/B]' % name
		windows = TextViewerXML('textviewer.xml', addonPath(), heading=heading, text=stats_lines)
		windows.run()
		del windows
	except Exception:
		error()


def upload_LogFile():
	from classyscrapers.modules.control import notification
	url = 'https://paste.kodi.tv/'
	log_file = joinPath(LOGPATH, 'classyscrapers.log')
	if not existsPath(log_file):
		return notification(message='Log File not found, likely logging is not enabled.')
	try:
		import requests
		from classyscrapers.modules.control import addonVersion, selectDialog
		f = open(log_file, 'r', encoding='utf-8', errors='ignore')
		text = f.read()
		f.close()
		UserAgent = 'ClassyScrapers %s' % addonVersion()
		response = requests.post(url + 'documents', data=text.encode('utf-8', errors='ignore'), headers={'User-Agent': UserAgent})
		if 'key' in response.json():
			result = url + response.json()['key']
			log('ClassyScrapers log file uploaded to: %s' % result)
			from sys import platform as sys_platform
			supported_platform = any(value in sys_platform for value in ('win32', 'linux2'))
			list = [('url:  %s' % str(result), str(result))]
			if supported_platform:
				list += [('  -- Copy url To Clipboard', ' ')]
			select = selectDialog([i[0] for i in list], lang(32059))
			if select >= 0 and 'Copy url To Clipboard' in list[select][0]:
				from classyscrapers.modules.source_utils import copy2clip
				copy2clip(list[0][1])
		elif 'message' in response.json():
			notification(message='ClassyScrapers Log upload failed: %s' % str(response.json()['message']))
			log('ClassyScrapers Log upload failed: %s' % str(response.json()['message']), level=LOGERROR)
		else:
			notification(message='ClassyScrapers Log upload failed')
			log('ClassyScrapers Log upload failed: %s' % response.text, level=LOGERROR)
	except Exception:
		error('ClassyScrapers log upload failed')
		notification(message='pastebin post failed: See log for more info')


def normalize(msg):
	try:
		import unicodedata
		msg = ''.join(c for c in unicodedata.normalize('NFKD', msg) if unicodedata.category(c) != 'Mn')
		return str(msg)
	except Exception:
		error()
		return msg
