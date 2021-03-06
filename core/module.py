# -*- coding: u8 -*-
"""
OWASP Maryam!

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSEdocs.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Based on the Recon-ng: https://github.com/lanmaster53/recon-ng

from __future__ import print_function
import os
import textwrap
# framework libs
from core import framework
from core.util import ahmia
from core.util import ask
from core.util import baidu
from core.util import bing
from core.util import cms_identify
from core.util import exalead
from core.util import frameworks_identify
from core.util import google
from core.util import hunter
from core.util import lang_identify
from core.util import metacrawler
from core.util import netcraft
from core.util import os_identify
from core.util import onionland
from core.util import page_parse
from core.util import rand_uagent
from core.util import reglib
from core.util import startpage
from core.util import urlib
from core.util import waf_identify
from core.util import web_scrap
from core.util import wapps
from core.util import yahoo
from core.util import yandex
from core.util import yippy

# =================================================
# MODULE CLASS
# =================================================


class BaseModule(framework.Framework):

	def __init__(self, params, query=None):
		framework.Framework.__init__(self, params)
		self.options = framework.Options()
		# register all other specified options
		if self.meta.get("options"):
			for option in self.meta["options"]:
				name, val, req, desc = option[:4]
				self.register_option(name, val, req, desc)
		self._reload = 0
		self._init_var()
		self._init_history()

	# ==================================================
	# OPTIONS METHODS
	# ==================================================

	def _get_source(self, params, query=None):
		if os.path.exists(params):
			sources = open(params).read().split()
		else:
			sources = [params]
		if not sources:
			raise framework.FrameworkException("Source contains no input.")
		return sources

	# ==================================================
	# SHOW METHODS
	# ==================================================

	def show_source(self):
		for path in [os.path.join(x, "modules", self._modulename) + self.module_extention for x in (self.app_path, self._home)]:
			if os.path.exists(path):
				filename = path
		with open(filename) as f:
			content = f.readlines()
			nums = [str(x) for x in range(1, len(content)+1)]
			num_len = len(max(nums, key=len))
			for num in nums:
				print("%s|%s" % (num.rjust(num_len), content[int(num)-1]), end='')

	def show_info(self):
		self.meta["path"] = os.path.join(
			"modules", self._modulename) + self.module_ext
		print('')
		# meta info
		for item in ["name", "path", "author", "version"]:
			if self.meta.get(item):
				print("%s: %s" % (item.title().rjust(10), self.meta[item]))
		print('')
		# description
		if "description" in self.meta:
			print("Description:")
			print("%s%s" % (self.spacer, textwrap.fill(
				self.meta["description"], 100, subsequent_indent=self.spacer)))
			print('')
		# options
		print("Options:", end='')
		self.show_options()
		# comments
		if "comments" in self.meta:
			print("Comments:")
			for comment in self.meta["comments"]:
				prefix = '* '
				if comment.startswith('\t'):
					prefix = self.spacer+'- '
					comment = comment[1:]
				print('%s%s' % (self.spacer, textwrap.fill(prefix+comment, 100, subsequent_indent=self.spacer)))
			print('')

		# sources
		if "sources" in self.meta:
			print("\nSources:\n\t%s"%("\n\t".join(self.meta["sources"])))

		# examples
		if "examples" in self.meta:
			print("Examples:\n\t%s"%("\n\t".join(self.meta["examples"])))
	def show_globals(self):
		self.show_options(self._global_options)

	# ==================================================
	# UTIL METHODS
	# ==================================================

	def ahmia(self, q):
		search = ahmia.main(self, q)
		return search

	def ask(self, q, limit=5):
		search = ask.main(self, q, limit)
		return search

	def baidu(self, q, limit=10):
		search = baidu.main(self, q, limit)
		return search

	def bing(self, q, limit=5, count=50):
		search = bing.main(self, q, limit, count)
		return search

	def cms_identify(self, content, headers):
		_cms = cms_identify.main(self, content, headers)
		return _cms

	def exalead(self, q, limit=3):
		search = exalead.main(self, q, limit)
		return search

	def frameworks_identify(self, content, headers):
		_frameworks = frameworks_identify.main(
			self, content, headers)
		return _frameworks

	def google(self, q, limit=5, count=50):
		search = google.main(self, q, limit, count)
		return search

	def hunter(self, q, key, limit=100):
		search = hunter.main(self, q, key, limit)
		return search

	def lang_identify(self, content, headers):
		_lang = lang_identify.main(self, content, headers)
		return _lang

	def metacrawler(self, q, limit=5):
		search = metacrawler.main(self, q, limit)
		return search

	def netcraft(self, q):
		search = netcraft.main(self, q)
		return search

	def os_identify(self, content, headers):
		_os = os_identify.main(self, content, headers)
		return _os

	def onionland(self, q, limit=5):
		search = onionland.main(self, q, limit)
		return search

	def page_parse(self, page):
		return page_parse.main(self, page)

	def rand_uagent(self):
		return rand_uagent.main(self)

	def reglib(self, page=None):
		return reglib.main(page)

	def urlib(self, url):
		return urlib.main(url)

	def wapps(self, q, page, headers):
		search = wapps.main(self, q, page, headers)
		return search

	def waf_identify(self, content, headers):
		_waf = waf_identify.main(self, content, headers)
		return _waf

	def web_scrap(self, url, force=False, debug=False, limit=20):
		search = web_scrap.main(self, url, force, debug, limit)
		return search

	def startpage(self, q, limit):
		search = startpage.main(self, q, limit)
		return search

	def yahoo(self, q, limit=5, cookie=None, count=50):
		search = yahoo.main(self, q, limit, count)
		return search

	def yandex(self, q, limit=5, cookie=None, count=50):
		search = yandex.main(self, q, limit, count)
		return search

	def yippy(self, q):
		search = yippy.main(self, q)
		return search

	# ==================================================
	# COMMAND METHODS
	# ==================================================

	def do_reload(self, params):
		'''Reloads the current module'''
		self._reload = 1
		return True

	def do_run(self, params):
		'''Runs the module'''
		spool_flag = 0
		try:
			if params:
				params = "start " + params
				self.do_spool(params)
				spool_flag = 1
			self._validate_options()
			self.module_pre()
			self.module_run()
			self.module_post()
		except KeyboardInterrupt:
			print('')
		except Exception:
			self.print_exception()
		finally:
			if spool_flag:
				self.do_spool("stop")
	def module_pre(self):
		pass

	def module_run(self):
		pass

	def module_post(self):
		pass
