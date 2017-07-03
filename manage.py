#!/usr/bin/env python
import os
import sys
import VideoWebsite.moviewer

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VideoWebsite.settings")

    from django.core.management import execute_from_command_line

    VideoWebsite.moviewer.conn_db()
    execute_from_command_line(sys.argv)
