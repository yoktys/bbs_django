# -*- coding: utf-8 -*-

import sys
import re

settings_regex = re.compile('--settings=bbs.settings.*')
settings_modules = filter(settings_regex.match, sys.argv)

# settings の指定がない場合はローカル設定を読み込む。
# manage.py の通常使い方を破壊したくないので、local 設定の指定以外は控える。
if len(settings_modules) == 0:
    from bbs.settings.local import *
