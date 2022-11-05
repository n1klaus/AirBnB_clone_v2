#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers"""
from fabric import *
import os


env.hosts = [54.152.232.208, 54.84.8.157]
env.user = ""
env.key = ""


def do_deploy(archive_path):
    """ Deploy archive to server """
    if (not os.path.exists(archive_path)):
        return False
    archive = str(os.path.dirname(archive_path))

    upload = put(archive, f"/tmp/{archive}")
    extract = sudo(
        f"tar xzvf /tmp/{archive} /data/web_static/releases/{archive}")
    delete = sudo(f"rm -f /tmp/{archive}")
    unlink = sudo("unlink /data/web_static/current")
    link = sudo(
        f"ln -s /data/web_static/releases/{archive} /data/web_static/current")
    if upload.succedded and extract.succeeded and delete.succeeded\
            and unlink.succeeded and link.succeeded:
        return True
    return False
