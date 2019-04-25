# -*- coding: utf-8 -*-
#
# git files deleter class.
# author: Toru Kageyama<kageyama@comona.co.jp>
# date: 2019/04/25
#

import os

class GitDeleter:

	# constants.
	FILE_PATH = 'file_path'
	IS_DIRECTORY = 'is_directory'
	GIT_KEEP = '.gitkeep'
	GIT_DIR = '.git'

	# variables.
	__yaml = None	# settings.yaml file.
	__xml = None	# GDriveGitXML object.
	__downloader = None	# GDriveDownloader object.
	__file_list = None	# file list.
	__delete_count = 0

	def __init__(self, downloader, xml, yaml):
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
		self.__yaml = yaml
		self.__xml = xml
		self.__downloader = downloader
		self.__file_list = []	# create list.


	def travarse_repository(self):
		'''
		travarse git local repository.
		'''
		for file, is_directory in self.__travarse_repository():
			#print('file found: {}, is directory: {}'.format(file, is_directory))
			if len(file) > 0:
				file_dict = {}
				file_dict[self.FILE_PATH] = file
				file_dict[self.IS_DIRECTORY] = is_directory
				self.__file_list.append(file_dict)


	def __travarse_repository(self):
		'''
		travarse git local repository.
		'''
		git_path = self.__xml.git_path()
		for root, dirs, files in os.walk(git_path):
			base_name = os.path.basename(root)
			if base_name != self.GIT_DIR:	# exclude .git directory.
				root_path = root
				root_path = root_path[len(git_path) : len(root)]
				yield root_path, True
				for file in files:
					fullpath = os.path.join(root, file)
					fullpath = fullpath[len(git_path) : len(fullpath)]
					yield fullpath, False


	def delete_not_in_gdrive(self):
		'''
		delete file from git repository, which is not in google drive
		'''
		git_path = self.__xml.git_path()
		for file_dict in reversed(self.__file_list):
			file_path = file_dict[self.FILE_PATH]
			is_directory = file_dict[self.IS_DIRECTORY]
			git_full_path = git_path + file_path	# create full path.
			if self.__downloader.is_exist(file_path):
				#print('file found: {}, is directory: {}, found: True'.format(file_path, is_directory))
				if is_directory:
					file_count = len(os.listdir(git_full_path))
					git_keep = os.path.join(git_full_path, self.GIT_KEEP)
					if file_count > 1:
						if os.path.exists(git_keep):
							print('{} file removed.'.format(git_keep))
							os.remove(git_keep)
							self.__delete_count = self.__delete_count + 1
					if file_count == 0:
						print('{} created.'.format(git_keep))
						open(git_keep, 'a').close()
						self.__downloader.increment_add_count()
			else:
				#print('Go to delete {} which is directory = {} is not found in google drive.'.format(file_path, is_directory))
				base_name = os.path.basename(git_full_path)
				if base_name != '.gitignore' and base_name != self.GIT_KEEP and git_full_path.startswith(git_path + '/' + self.GIT_DIR) == False:
					if is_directory:
						print('{} directory removed.'.format(git_full_path))
						os.rmdir(git_full_path)
					else:
						print('{} file removed.'.format(git_full_path))
						os.remove(git_full_path)
					self.__delete_count = self.__delete_count + 1


	def delete_count(self):
		'''
		get delete count.
		Returns
		-------
		self.__delete_count: int
			delete count.
		'''
		return self.__delete_count
