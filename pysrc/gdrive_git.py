#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# goole drive download script for git commit/push.
# author: Toru Kageyama<kageyama@comona.co.jp>
# date: 2019/04/24
#

import sys
import yaml

# pip install google-api-python-client
# pip install PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# classes from this project.
from gdrive_git_xml import GDriveGitXML
from gdrive_downloader import GDriveDownloader
from git_deleter import GitDeleter
from git_committer import GitCommitter

if __name__ == '__main__':
	try:
		# google authenticate.
		gauth = GoogleAuth()
		gauth.CommandLineAuth()
		drive = GoogleDrive(gauth)

		# read settings.yaml file on current directory.
		f = open('settings.yaml', 'r')
		settings_yaml = yaml.load(f, Loader=yaml.FullLoader)
		xml = GDriveGitXML(settings_yaml)

		# download from google drive.
		downloader = GDriveDownloader(drive, xml, settings_yaml)
		downloader.download()
		#print("modify_count = {}, add_count = {}".format(downloader.modify_count(), downloader.add_count()))

		# delete git local repository file, if not in google drive any more.
		deleter = GitDeleter(downloader, xml, settings_yaml)
		deleter.travarse_repository()
		deleter.delete_not_in_gdrive()

		# commit git if something updated.
		updated = downloader.modify_count() + downloader.add_count() + deleter.delete_count()
		if updated > 0:
			committer = GitCommitter(xml)
			committer.commit()

		sys.exit()	# exit normal.

	except Exception as e:
		print(e)
		sys.exit(1)	# exit error.
