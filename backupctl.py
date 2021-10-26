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
    logging.basicConfig(
        filename=journal,
        format=' Date-Time : %(asctime)s %(message)s',
        level=logging.DEBUG)
    log = logging.getLogger(__name__)
    if os.path.exists(directory) and os.path.exists(output):
        archive_do = True
        archive_date = datetime.datetime.now(tz=None)
        name = str(os.path.basename(directory)) + "_" + archive_date.strftime("%Y-%m-%d_%H:%M:%S")
        extension = archive
        if archive == "gztar":
            extension = "tar.gz"
        elif archive == "bztar":
            extension = "tar.bz2"
        elif archive == "xztar":
            extension = "tar.xz"
        archive_path = output + "/" + f"{name}.{extension}"
        try:
            shutil.make_archive(name, archive, directory)
            shutil.move(f"{name}.{extension}", output)
        except OSError as er:
            sys.stderr.write(str(er))
            archive_do = False
        if archive_do:
            sys.stdout.write(archive_path)
            log.info('Directory: ' + directory + 'Archive: ' + archive_path + ' Status: success')
        else:
            log.info('Directory: ' + directory + ' Status: fail')
    else:
        sys.stderr.write('Directory or output not exist')
        log.info('Directory: ' + directory + ' Status: fail')


if __name__ == '__main__':
    try:
        create_archive()
    except ValueError as err:
        sys.stderr.write(str(err))
    except FileNotFoundError as err:
        sys.stderr.write(str(err))
