# -*- coding: utf-8 -*-
#
# git committer class.
# author: Toru Kageyama<kageyama@comona.co.jp>
# date: 2019/04/25
#

import os
import commands
from datetime import datetime as dt

class GitCommitter:

	# variables.
	__xml = None	# GDriveGitXML object.

	def __init__(self, xml):
		'''
		constructor
		Parameters
		----------
		downloader GDriveDownloader:
			google drive downloader.
		xml GDriveGitXML:
			setting XML object.
		yaml dict:
			content of settings.yaml file.
		'''
		self.__xml = xml


	def commit(self):
		'''
		commit git.
		'''
		print(self.__xml.git_command())
		os.chdir(self.__xml.git_path())

		res = commands.getoutput(self.__xml.git_command() + ' add -A')
		print(res)

		now = dt.now()
		comment = now.strftime(self.__xml.git_comment_format())
		res = commands.getoutput(self.__xml.git_command() + ' commit -m "{}"'.format(comment))
		print(res)

		res = commands.getoutput(self.__xml.git_command() + ' push')
		print(res)
