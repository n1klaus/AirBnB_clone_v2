#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers"""
from fabric.api import *
import os


env.hosts = ["54.160.127.10", "34.207.156.177"]


def do_deploy(archive_path):
    """ Deploy archive to server """
    if (not os.path.exists(archive_path)):
        return False
    archive_name = os.path.split(archive_path)[-1]
    upload = put("{0}".format(os.path.realpath(archive_path)),
                 "/tmp/{0}".format(archive_name))
    create_dir = run("sudo mkdir -p /data/web_static/releases/{0}"
                     .format(archive_name.split('.')[0]))
    extract = run("sudo tar xzvf /tmp/{0} -C /data/web_static/releases/{1}"
                  .format(archive_name, archive_name.split('.')[0]))
    move = run("sudo mv -f /data/web_static/releases/{0}/web_static/* \
               /data/web_static/releases/{0}/"
               .format(archive_name.split('.')[0]))
    delete = run(
        "sudo rm -rf /tmp/{0} /data/web_static/releases/{1}/web_static/"
        .format(archive_name, archive_name.split('.')[0]))
    unlink = run("sudo unlink /data/web_static/current")
    link = run(
        "sudo ln -s /data/web_static/releases/{0} /data/web_static/current".
        format(archive_name.split('.')[0]))
    if upload.succeeded and extract.succeeded and move.succeeded and\
            delete.succeeded and unlink.succeeded and link.succeeded:
        print("New version deployed!")
        return True
    return False
