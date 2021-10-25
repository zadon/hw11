#!/usr/bin/env python3
import os
import sys
import datetime
import shutil
import click
import logging


@click.command()
@click.option('--directory', help='Directory to archive')
@click.option('--output', help='Output directory')
@click.option('-a', '--archive', default='gztar', help='Archiver')
@click.option('-j', '--journal', default='journal.csv', help='File of journal')
def create_archive(directory, output, archive, journal):
    archive_do = True
    logging.basicConfig(
        filename=journal,
        format=' Date-Time : %(asctime)s Status: %(message)s',
        level=logging.DEBUG)
    log = logging.getLogger(__name__)
    archive_date = datetime.datetime.now(tz=None)
    name = str(os.path.basename(directory)) + "_" + archive_date.strftime("%Y-%m-%d_%H:%M:%S")
    format_ = archive
    try:
        shutil.make_archive(name, format_, directory, )
    except FileNotFoundError:
        archive_do = False
        sys.stderr.write("Directory not found")
    except MemoryError:
        archive_do = False
        sys.stderr.write("Memory error")
    extension = format_
    if format_ == "gztar":
        extension = "tar.gz"
    elif format_ == "bztar":
        extension = "tar.bz2"
    elif format_ == "xztar":
        extension = "tar.xz"
    try:
        shutil.move(f"{name}.{extension}", output)
    except FileExistsError:
        archive_do = False
        sys.stderr.write("already exists")
    except FileNotFoundError:
        archive_do = False
    if archive_do:
        sys.stdout.write(output + "/" + f"{name}.{extension}")
        log.info("success")
    else:
        log.info("fail")


if __name__ == '__main__':
    create_archive()
