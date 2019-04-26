gdrive_git
====

Overview

## Version
0.1.0

## Description
Provide versioning to google drive folder with git.

## Requirement
* Mac OSX, Linux
* Python 2.7
* google-api-python-client, do pip install or any other equivalent.
* PyDrive, do pip install or any other equivalent.
* your command line git tool is properly installed.

## Usage
* prepare your google drive git repository with $ git init --bare --shared ... to your git central repository.
* git clone your google drive repository into your computer.
* git clone this project repository into your computer.
* mkdir your gdrive_git/ working directory somewhere in your computer.
* copy contents of misc/ directory of this project to your gdrive_git/ working directory.
* log in to your google developer console and enable google drive API.
* generate app and obtain client-id and client-secret.
* enable google drive API to your app.
* past client-id into \_\_YOUR_APP_CLIENT_ID\_\_ and client-secret into \_\_YOUR_APP_CLIENT_SECRET\_\_ in settings.yaml in your gdrive_git/ working directory.
* replace \_\_YOUR_GOOGLE_DRIVE_FOLDER_ID_TO_GIT\_\_ with your google folder id, which you want to provide versioning. you better not to set the root of your google drive. you can obtain it with log in to your gooogle drive with your account, and browse your target directory. the URL is something like 'https://drive.google.com/drive/folders/YOUR-GOOGLE-DRIVE-FOLDER-ID'.
* replace \_\_YOUR_LOCAL_GIT_REPOSITORY_PATH\_\_ with your local git repository path in settings.yaml in your gdrive_git/ working directory.
* you are better to set full path of your git command line tool into gdrive_git -> git -> command element's text of settings.yaml in your gdrive_git/ working directory. you can obtain it with $ which git.
* replace \_\_YOUR_GDRIVE_GIT_PYTHON_DIR_PATH\_\_ with your gdrive_git python source diretory path in gdrive_git.sh in your gdrive_git/ working directory.
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
* you can change above setting to edit settings.yaml in your gdrive_git/ working directory. something like ...
```
    ...
    gdoc:
      # google documents convert configurations.
      # google document to microsoft word.
      -
        from: application/vnd.google-apps.document
        to: pplication/vnd.openxmlformats-officedocument.wordprocessingml.document
        extension: docx
        ...
```
* you can find exportable formats in https://developers.google.com/drive/api/v3/manage-downloads.

## Licence

[MIT](https://github.com/t-kageyama/gdrive_git/blob/master/LICENSE)

## Author

[t-kageyama](https://github.com/t-kageyama)
