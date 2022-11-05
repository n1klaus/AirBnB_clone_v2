#!/usr/bin/python3
""" Fabric script that generates a .tgz archive
    from the contents of the web_static folder
"""
from fabric import *
import os


def do_pack():
    """ Compress files into tar archive """
    v = local("mkdir -p versions")
    result = local(
        "tar -cvzf versions/web_static_$(date + '%Y%m%d%H%M%S').tgz\
        web_static")
    if result.stdout == 0:
        return None
    return os.path.realpath('versions')
