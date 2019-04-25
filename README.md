gdrive_git
====

Overview

## Description
Provide versioning to google drive folder with git.

## Requirement
Mac OSX, Linux
Python 2.7
google-api-python-client
PyDrive
do pip install or any other equivalent.
your command line git tool is properly installed.

## Usage
* prepare your google drive git repository with $ git init --bare --shared ... to your git central repository.
* git clone your google drive repository into your computer.
* git clone this project repository into your computer.
* mkdir your gdrive_git/ working directory somewhere in your computer.
* copy contents of misc/ directory of this project to your gdrive_git/ working directory.
* log in to your google developer console and enable google drive API.
* generate app and obtain client-id and client-secret.
* past client-id into __YOUR_APP_CLIENT_ID__ and client-secret into __YOUR_APP_CLIENT_SECRET__ in settings.yaml in your gdrive_git/ working directory.
* replace __YOUR_GOOGLE_DRIVE_FOLDER_ID_TO_GIT__ with your google folder id, which you want to provide versioning. you better not to set the root of your google drive. you can obtain it with log in to your gooogle drive with your account, and browse your target directory. the URL is something like 'https://drive.google.com/drive/folders/<<YOUR-GOOGLE-DRIVE-FOLDER-ID>>'.
* replace __YOUR_LOCAL_GIT_REPOSITORY_PATH__ with your local git repository path in gdrive_git.xml in your gdrive_git/ working directory.
* you are better to set full path of your git command line tool into gdrive_git -> git -> command element's text of gdrive_git.xml in your gdrive_git/ working directory. you can obtain it with $ which git.
* replace __YOUR_GDRIVE_GIT_PYTHON_DIR_PATH__ with your gdrive_git python source diretory path in gdrive_git.sh in your gdrive_git/ working directory.
* go to your gdrive_git/ working directory.
* then $ ./gdrive_git.sh
* gdrive_git will prompt you google api URL and access it with your favorite browser. you can obtain verification code, then copy and past into your gdrive_git tool input and push enter key.
* at the first time, your git command will ask you your user id and password of git repository, if git authentication required.
* you will find, your git repository contained with your google drive contents.

* some google documents will export into other formats, because you can only download zero byte files.
* gdrive_git tool initially provides convert file format like followings.
* google document -> open office document (*.odt).
* google sheet -> open office spread sheet (*.ods).
* google slide -> open office presentation (*.odp).
* google drawing -> SVG (*.svg).
* google apps scripts -> script JSON (*.json).
* google map -> google earth KML (*.kml).
* you can change above setting to edit gdrive_git.xml in your gdrive_git/ working directory. something like ...
            ...
			<converts><!-- google documents convert configurations. -->
				<convert><!-- google document to microsoft word. -->
					<from>application/vnd.google-apps.document</from>
					<to>pplication/vnd.openxmlformats-officedocument.wordprocessingml.document</to>
					<extension>docx</extension>
				</convert>
                ...
* you can find exportable formats in https://developers.google.com/drive/api/v3/manage-downloads.

## Licence

Copyright 2019 Toru Kageyama

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Author

[t-kageyama](https://github.com/t-kageyama)
