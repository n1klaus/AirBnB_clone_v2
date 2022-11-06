#!/usr/bin/python3
""" 
    Fabric script that creates and distributes an archive to your web servers
"""
from fabric.api import *
import os

env.hosts = ["54.160.127.10", "34.207.156.177"]

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
    print("web_static packed: versions/{0} -> {1}Bytes".
          format(_file, file_info[4]))
    env.archive_path = os.path.realpath("{0}".format(_file))
    return env.archive_path

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

@task
def deploy():
    """ Full deployment """
    archive_path = do_pack()
    if archive_path:
        result = do_deploy(archive_path)
        if result:
            return True
    return False
