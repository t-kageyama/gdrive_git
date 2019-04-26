# -*- coding: utf-8 -*-
#
# goole drive download XML settings class.
# author: Toru Kageyama<kageyama@comona.co.jp>
# date: 2019/04/24
#

import os
import xml.etree.ElementTree as ET

class GDriveGitXML:

	# constants.
	FROM = 'from'
	TO = 'to'
	EXTENSION = 'extension'
	DEFAULT_COMMENT = 'Committed at %F %T.'
	DEFAULT_COMMAND = 'git'
	XML_FILE_ELEMENT = 'xml_file'
	DRIVE_GIT_ELEMENT = 'gdrive_git'
	GDRIVE_ELEMENT = 'gdrive'
	FOLDER_ELEMENT = 'folder'
	ID_ELEMENT = 'id'
	GDOC_ELEMENT = 'gdoc'
	GIT_ELEMENT = DEFAULT_COMMAND
	REPOSITORY_ELEMENT = 'repository'
	COMMAND_ELEMENT = 'command'
	COMMENT_ELEMENT = 'comment'

	# variables.
	__xml_path = None	# XML file path.
	__folder_id = None	# target folder id.
	__converts = {}		# converts dictionary.
	__git_path = None	# git local repository path.
	__git_command = None	# git command.
	__git_format = None	# format.


	def __init__(self, yaml):
		'''
		constructor
		Parameters
		----------
		yaml dict:
			content of settings.yaml file.
		'''
		self.__git_command = self.DEFAULT_COMMAND
		self.__git_format = self.DEFAULT_COMMENT

		# read XML file.
		if not self.XML_FILE_ELEMENT in yaml:
			self.__load_from_yaml(yaml)
		else:
			self.__xml_path = yaml[self.XML_FILE_ELEMENT]
			self.__load_from_xml()


	def __load_from_yaml(self, yaml):
		'''
		load from YAML file.
		yaml dict:
			content of settings.yaml file.
		'''
		gdrive_git = yaml[self.DRIVE_GIT_ELEMENT]
		gdrive = gdrive_git[self.GDRIVE_ELEMENT]
		folder = gdrive[self.FOLDER_ELEMENT]
		self.__folder_id = folder[self.ID_ELEMENT]
		if self.__folder_id is None or len(self.__folder_id) < 1:
			raise ValueError('target folder id not found in settings.yaml file!')

		# converts list.
		convert_list = gdoc = gdrive[self.GDOC_ELEMENT]
		index = 1
		for convert in convert_list:
			conv_dict = {}
			from_val = convert[self.FROM]
			if from_val == None or len(from_val) < 1:
				raise ValueError('from value not found in settings.yaml file at No.{} convert!'.format(index))
			to_val = convert[self.TO]
			if to_val == None or len(to_val) < 1:
				raise ValueError('to value not found in settings.yaml file at No.{} convert!'.format(index))
			extension = convert[self.EXTENSION]
			if extension == None or len(extension) < 1:
				raise ValueError('extension value not found in settings.yaml file at No.{} convert!'.format(index))
			conv_dict[self.FROM] = from_val
			conv_dict[self.TO] = to_val
			conv_dict[self.EXTENSION] = extension
			if from_val not in self.__converts:
				self.__converts[from_val] = conv_dict
			else:
				raise ValueError('duplicate entry for {} in settings.yaml file at No.{} convert!'.format(from_val, index))
			index = index + 1

		# getting git local repository path.
		git = gdrive_git[self.GIT_ELEMENT]
		repository = git[self.REPOSITORY_ELEMENT]
		self.__git_path = os.path.abspath(repository)
		if self.__git_path is None or len(self.__git_path) < 1:
			raise ValueError('local git repository path not found in settings.yaml file!')
		if not os.path.isdir(self.__git_path):	# check directory exists.
			raise ValueError('local git repository path {} in settings.yaml file not exist!'.format(self.__git_path))

		command_line = git[self.COMMAND_ELEMENT]
		if not command_line is None and len(command_line) > 0:
			self.__git_command = command_line
		comment_format = git[self.COMMENT_ELEMENT]
		if not comment_format is None and len(comment_format) > 0:
			self.__git_format = comment_format


	def __load_from_xml(self):
		'''
		load from XML file.
		'''
		gdrive_git = ET.parse(self.__xml_path)
		gdrive = gdrive_git.find(self.GDRIVE_ELEMENT)

		# getting target folder id.
		folder = gdrive.find(self.FOLDER_ELEMENT)
		folder_id = folder.find(self.ID_ELEMENT)
		self.__folder_id = folder_id.text
		if self.__folder_id is None or len(self.__folder_id) < 1:
			raise ValueError('target folder id not found in XML file {}!'.format(self.__xml_path))

		# converts list.
		gdoc = gdrive.find(self.GDOC_ELEMENT)
		convert_list = gdoc.findall('converts/convert')
		index = 1
		for convert in convert_list:
			conv_dict = {}
			from_val = convert.find(self.FROM).text
			if from_val == None or len(from_val) < 1:
				raise ValueError('from value not found in XML file {} at No.{} convert!'.format(self.__xml_path, index))
			to_val = convert.find(self.TO).text
			if to_val == None or len(to_val) < 1:
				raise ValueError('to value not found in XML file {} at No.{} convert!'.format(self.__xml_path, index))
			extension = convert.find(self.EXTENSION).text
			if extension == None or len(extension) < 1:
				raise ValueError('extension value not found in XML file {} at No.{} convert!'.format(self.__xml_path, index))
			conv_dict[self.FROM] = from_val
			conv_dict[self.TO] = to_val
			conv_dict[self.EXTENSION] = extension
			if from_val not in self.__converts:
				self.__converts[from_val] = conv_dict
			else:
				raise ValueError('duplicate entry for {} in XML file {} at No.{} convert!'.format(from_val, self.__xml_path, index))
			index = index + 1

		# getting git local repository path.
		git = gdrive_git.find(self.GIT_ELEMENT)
		repository = git.find(self.REPOSITORY_ELEMENT)
		self.__git_path = os.path.abspath(repository.text)
		if self.__git_path is None or len(self.__git_path) < 1:
			raise ValueError('local git repository path not found in XML file {}!'.format(self.__xml_path))
		if not os.path.isdir(self.__git_path):	# check directory exists.
			raise ValueError('local git repository path {} in XML file {} not exist!'.format(self.__git_path, self.__xml_path))

		command = git.find(self.COMMAND_ELEMENT)
		if not command is None:
			command_line = command.text
			if not command_line is None and len(command_line) > 0:
				self.__git_command = command_line
		comment = git.find(self.COMMENT_ELEMENT)
		if not comment is None:
			comment_format = comment.text
			if not comment_format is None and len(comment_format) > 0:
				self.__git_format = comment_format


	def folder_id(self):
		'''
		get target folder id.
		Returns
		-------
		self.__folder_id: string
			target folder id.
		'''
		return self.__folder_id


	def git_path(self):
		'''
		get local git repository path.
		Returns
		-------
		self.__git_path: string
			local git repository path.
		'''
		return self.__git_path


	def git_command(self):
		'''
		get git command line.
		Returns
		-------
		self.__git_command: string
			git command line.
		'''
		return self.__git_command


	def git_comment_format(self):
		'''
		get git comment format.
		Returns
		-------
		self.__git_command: string
			git comment format.
		'''
		return self.__git_format


	def mime_type(self, orig_mime_type):
		'''
		get MIME type to download.
		Parameters
		----------
		orig_mime_type string:
			original MIME type.
		Returns
		-------
		mime_type: string
			MIME type string.
		'''
		if orig_mime_type in self.__converts:
			return self.__converts[orig_mime_type][self.TO]
		else:
			return orig_mime_type


	def extension(self, orig_mime_type):
		'''
		get file extension to download.
		Parameters
		----------
		orig_mime_type string:
			original MIME type.
		Returns
		-------
		mime_type: string
			MIME type string.
		'''
		if orig_mime_type in self.__converts:
			return self.__converts[orig_mime_type][self.EXTENSION]
		else:
			return None
