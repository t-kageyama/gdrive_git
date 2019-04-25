#!/bin/sh
#
# google drive -> git commit shell script.
# author: kageyama<kageyama@comona.co.jp>
# date: 2019/04/25
#

MY_DIR_NAME=`dirname $0`
SHELL_SCRIP_DIR=`cd $MY_DIR_NAME;pwd`
cd $SHELL_SCRIP_DIR

__YOUR_GDRIVE_GIT_PYTHON_DIR_PATH__/gdrive_git.py
