#!/usr/bin/env python3
"""Module: 1-pack_web_static"""

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if successfully generated, None otherwise.
    """
    # Create the versions directory if it doesn't exist
    if not os.path.exists("versions"):
        local("mkdir -p versions")

    # Generate archive path
    now = datetime.utcnow()
    archive_path = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)

    # Compress web_static contents into the archive
    result = local("tar -cvzf {} web_static".format(archive_path))

    # Check if the archive was created successfully
    if result.succeeded:
        return archive_path
    else:
        return None

if __name__ == "__main__":
    # Run the do_pack function when the script is executed
    do_pack()
