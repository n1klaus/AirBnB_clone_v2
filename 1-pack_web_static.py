#!/usr/bin/python3
""" Fabric script that generates a .tgz archive
    from the contents of the web_static folder
"""
from fabric.api import *
import os


def do_pack():
    """
       Compress files into tar archive

       Returns: the archive path if the archive has been correctly generated,
                otherwise None
    """
    local("mkdir -p versions")
    _date = local("echo $(date +'%Y%m%d%H%M%S')", capture=True)
    _file = "web_static_{0}.tgz".format(_date.stdout)
    output = local("tar -cvzf versions/{0} web_static".format(_file))
    if output.failed:
        return None
    file_info = local("ls -l versions/{0}".format(_file), capture=True)
    file_info = str(file_info.stdout).split(' ')
    print("web_static packed: versions/{0} -> {1}Bytes".format(_file, file_info[4]))
    env.archive_path = os.path.realpath("{0}".format(_file))
    return env.archive_path
