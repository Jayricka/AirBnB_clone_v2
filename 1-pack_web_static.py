#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the contents of the web_static"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Creates a compressed archive from the web_static folder"""
    if not os.path.exists("versions"):
        os.makedirs("versions")
    
    archive_name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".tgz"
    print("Packing web_static to {}".format(archive_name))
    
    result = local("tar -cvzf versions/{} web_static".format(archive_name))
    
    if result.succeeded:
        print("web_static packed: versions/{} -> {}Bytes".format(archive_name, os.path.getsize("versions/" + archive_name)))
        return "versions/{}".format(archive_name)
    else:
        return None

if __name__ == "__main__":
    do_pack()
