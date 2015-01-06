#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from vmbundler import commands

# 依存関係を調べる。異常があった場合はアプリを終了させる。
commands.inspect()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
