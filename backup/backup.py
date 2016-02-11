#!/usr/bin/env python3import osimport datetimeimport loggingimport shutilimport tarfileimport gzipfrom ftplib import FTP# Handle Configfrom backup_config import CONFIGHOST = CONFIG['host']USER = CONFIG['user']PASSWD = CONFIG['passwd']LOG_PATH = CONFIG['log']PATH = CONFIG['path']DATETIME_FORMAT = CONFIG['format']KEEP = CONFIG['keep']# Configure logginglogging.basicConfig(    filename=LOG_PATH,    level=logging.DEBUG,    format='%(asctime)s - %(levelname)s:%(message)s')def dt():    """    Returns a current datetime string    :return: String representing .now().    """    return datetime.datetime.now().strftime(DATETIME_FORMAT)def get_dt(fn):    """    Gets a datetime object form the given filename    :param fn: A filename with an appended date generated by this script file    :return: Datetime object    """    return datetime.datetime.strptime(fn[:19], DATETIME_FORMAT)def sort(x, lis):    """    Check to see if the dated filename is newer than any of the dated filenames    in the given list and if so, replace the first item in the list that it is bigger    than.    :param x: Dated filename to check.    :param lis: List of dated filenames to compare against x    :return: True if x added to keep list, else None    """    for i, y in enumerate(lis):        if get_dt(x) > get_dt(y):            lis[i] = x            return Truedef clean(files, num):    """    Deletes all but the given number of the newest files.    :param files: A list of file names    :param num: Maximum number of iterations    :return: List of files to delete    """    # First see if any cleaning needs to be done.    if len(files) <= num:        return []    logging.info('Cleaning old files')    # Generate a list of filenames to keep.    keep = files[:num]    for x in files:        sort(x, keep)    logging.info('Keeping: {0}'.format(keep))    # Subtract and return list of files to keep from list of all files.    return list(set(files) - set(keep))logging.info('Script started')# Prepare file for backup and append the current DateTime to the files.dt_file = dt()filename_tar = '{0}__dbdata.tar'.format(dt_file)filename = '{0}__dbdata.gz'.format(dt_file)# Make an archive (tar file).with tarfile.open(filename_tar, 'w') as tar:    tar.add(PATH)    logging.info('Archive ({0}) created'.format(filename_tar))# Put the archive in a compressed file (gzip).with open(filename_tar, 'rb') as f_in, gzip.open(filename, 'wb') as f_out:    shutil.copyfileobj(f_in, f_out)    logging.info('Archive ({0}) moved to compressed file ({1})'.format(filename_tar, filename))# Delete the archive.os.remove(filename_tar)logging.info('Archive ({0}) deleted'.format(filename_tar))# Send file to FTP server.logging.info('Connecting to host ({0})...'.format(CONFIG['host']))with FTP(host=HOST, user=USER, passwd=PASSWD) as ftp:    logging.info('Connected to host ({0}).'.format(CONFIG['host']))    with open(filename, 'rb') as archive:        logging.info('Compressed file uploading ({0})...'.format(filename))        ftp.storbinary('STOR ' + filename, archive)        logging.info('Compressed file uploaded.')    # Cleans the FTP folder of old files    files_delete = clean([i[0] for i in ftp.mlsd()], KEEP)    for file in files_delete:        logging.info('Deleting old file ({0})'.format(file))        ftp.delete(file)    ftp.quit()# Delete the compressed file.os.remove(filename)logging.info('Compressed file ({0}) deleted'.format(filename))logging.info('Script finished')