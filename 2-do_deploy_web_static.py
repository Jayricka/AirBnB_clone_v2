#!/usr/bin/env python3
"""Fabric script that distributes an archive to web servers"""

from fabric.api import env, put, run
from datetime import datetime
import os
import configparser

# Load configuration from the config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Set environment variables from the configuration file
env.user = config.get('web_servers', 'user', fallback='ubuntu')
env.key_filename = config.get('web_servers', 'private_key_path', fallback='/home/ricka-g/my_ssh_private_key')

# Read the list of web servers from the configuration file
web_server_1 = config.get('web_servers', 'web_server_1', fallback='')
web_server_2 = config.get('web_servers', 'web_server_2', fallback='')

# Set the list of web servers
env.hosts = [web_server_1, web_server_2]


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the folder /data/web_static/releases/
        archive_filename = os.path.basename(archive_path)
        release_folder = '/data/web_static/releases/{}'.format(os.path.splitext(archive_filename)[0])
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        # Move the contents of the release folder to the proper location
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Delete the empty web_static folder
        run('rm -rf {}/web_static'.format(release_folder))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link /data/web_static/current
        run('ln -s {} /data/web_static/current'.format(release_folder))

        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    archive_path = 'versions/web_static_{}.tgz'.format(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = do_deploy(archive_path)
    if result:
        print('New version deployed!')
    else:
        print('Deployment failed!')
