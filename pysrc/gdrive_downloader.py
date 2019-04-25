# -*- coding: utf-8 -*-
#
# goole drive downloaders class.
# author: Toru Kageyama<kageyama@comona.co.jp>
# date: 2019/04/24
#

import os
import time
import calendar
import httplib2
from datetime import datetime as dt, timedelta

from oauth2client.file import Storage
from apiclient.discovery import build
from apiclient.http import MediaIoBaseDownload

class GDriveDownloader:

	# constants.
	ID = 'id'
	MIME_TYPE = 'mimeType'
	TITLE = 'title'
	UTF_8 = 'utf-8'
	GOOGLE_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

	# variables.
	__yaml = None	# settings.yaml file.
	__drive = None	# google drive.
	__xml = None	# GDriveGitXML object.
	__file_dict = None	# file dictionary.
	__drive_service = None	# google drive service.
	__modify_count = 0	# modify count.
	__add_count = 0		# add count.

	def __init__(self, drive, xml, yaml):
		'''
		constructor
		Parameters
		----------
		drive GoogleDrive:
			google drive object.
		xml GDriveGitXML:
			setting XML object.
		yaml dict:
			content of settings.yaml file.
		'''
		self.__yaml = yaml
		self.__drive = drive
		self.__xml = xml
		self.__file_dict = {}
		storage = Storage(self.__yaml['save_credentials_file'])
		credentials = storage.get()
		http = httplib2.Http()
		http = credentials.authorize(http)
		self.__drive_service = build('drive', 'v2', http=http)


	def download(self):
		'''
		download from google drive.
		'''
		parent = ""
		self.__download(self.__xml.folder_id(), parent)


	def __download(self, folder_id, parent):
		'''
		download from google drive.
		Parameters
		----------
		folder_id string:
			google drive folder id.
		parent string:
			parent folder name.
		'''
		if len(parent) > 0:	# create directory.
			dir_path = self.__xml.git_path() + parent
			if not os.path.exists(dir_path):
  				os.makedirs(dir_path)

		max_results = 100
		query = "'{}' in parents and trashed=false".format(folder_id)
		lister = self.__drive.ListFile({"q": query, 'maxResults': max_results}).GetList()
		for item in lister:
			title = item[self.TITLE].encode(self.UTF_8)
			mime_type = item[self.MIME_TYPE]
			fullpath = parent + "/" + title
			file_id = item[self.ID]
			if mime_type == 'application/vnd.google-apps.folder':
				self.__file_to_dictionary(item, fullpath)
				self.__download(file_id, fullpath)
			else:
				self.__download_file(parent, item)


	def __download_file(self, parent, item):
		'''
		download file from google drive.
		Parameters
		----------
		parent string:
			parent folder name.
		item dict:
			download item.
		'''
		dir_path = self.__xml.git_path() + parent
		add = 0
		modify = 0

		file_id = item[self.ID]
		orig_mime_type = item[self.MIME_TYPE]
		mime_type = self.__xml.mime_type(orig_mime_type)
		title = item[self.TITLE].encode(self.UTF_8)

		#modify_date = dt.strptime(item["modifiedDate"], self.GOOGLE_DATE_FORMAT).replace(microsecond=0) + timedelta(hours=self.__hour_delta)
		modify_date = self.__conv_datetime(item['modifiedDate'])

		if orig_mime_type != mime_type:
			request = self.__drive_service.files().export_media(fileId=file_id, mimeType=mime_type)	# convert download.
		else:
			request = self.__drive_service.files().get_media(fileId=file_id)	# direct download.

		outfile = os.path.join(dir_path, title)
		new_extension = self.__xml.extension(orig_mime_type)
		gdrive_path = parent + '/' + title
		if not new_extension is None:
			outfile = outfile + '.' + new_extension
			gdrive_path = gdrive_path + '.' + new_extension

		self.__file_to_dictionary(item, gdrive_path)

		# compare file date and google drive modify date.
		if os.path.exists(outfile):
			file_date = dt.fromtimestamp(os.stat(outfile).st_mtime)
			#print("file_date = {}, modify_date = {}".format(file_date, modify_date))
			if file_date >= modify_date:
				print('{} not modified!'.format(outfile))
				return
			modify = 1
		else:
			add = 1

		print('{} start downloading!'.format(outfile))

		fh = open(outfile, 'w')
		downloader = MediaIoBaseDownload(fh, request)
		done = False
		while done is False:
			status, done = downloader.next_chunk()

		fh.close()
		print("{} finish download!".format(outfile))

		#access_date = dt.strptime(item["lastViewedByMeDate"], self.GOOGLE_DATE_FORMAT).replace(microsecond=0) + timedelta(hours=self.__hour_delta)
		access_date = self.__conv_datetime(item['lastViewedByMeDate'])
		if access_date < modify_date:
			access_date = modify_date
		os.utime(outfile, (time.mktime(access_date.timetuple()), time.mktime(modify_date.timetuple())))

		self.__modify_count = self.__modify_count + modify
		self.__add_count = self.__add_count + add


	def __conv_datetime(self, date_time):
		'''
		convert date time from UTC to local time zone.
		Parameters
		----------
		date_time string:
			date time string from google drive.
		Returns
		-------
		timestamp: datetime
			local time zone date time.
		'''
		gloogle_date = dt.strptime(date_time, self.GOOGLE_DATE_FORMAT).replace(microsecond=0)	# remove microseconds for file date compare.
		timestamp = calendar.timegm(gloogle_date.timetuple())
		return dt.fromtimestamp(timestamp)


	def modify_count(self):
		'''
		get modify count.
		Returns
		-------
		self.__modify_count: int
			modify count.
		'''
		return self.__modify_count


	def add_count(self):
		'''
		get add count.
		Returns
		-------
		self.__add_count: int
			add count.
		'''
		return self.__add_count


	def increment_add_count(self):
		'''
		increment add count.
		'''
		self.__add_count = self.__add_count + 1


	def __file_to_dictionary(self, item, fullpath):
		'''
		add google drive file to file directory.
		Parameters
		-------
		item: dict
			file dictionary of google drive.
		fullpath: string
			fullpath name for downloaded item.
		'''
		if not fullpath in self.__file_dict:
				self.__file_dict[fullpath] = item
		else:
			raise ValueError('Same file path {} found in google drive!'.format(fullpath))


	def is_exist(self, path):
		'''
		check in directory or not.
		Parameters
		-------
		path: string
			file path which is exist or not in google drive.
		Returns
		-------
		self.__file_dict: Boolean
			is exit or not.
		'''
		return path in self.__file_dict