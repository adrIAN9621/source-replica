import os
import sys
import shutil
import time

source_folder = input('Enter source folder path: ')
replica_folder = input('Enter replica folder path: ')
interval = int(input('Enter synchronization interval (in seconds): '))
log_file_path = input('Enter log file path: ')

def sync_folders(source_folder, replica_folder):
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    for item in os.listdir(source_folder):
        source_path = os.path.join(source_folder, item)
        replica_path = os.path.join(replica_folder, item)

        
        if os.path.isdir(source_path):
            sync_folders(source_path, replica_path)
        else:
            if not os.path.exists(replica_path) or \
                    (os.path.exists(replica_path) and
                     os.stat(source_path).st_mtime - os.stat(replica_path).st_mtime > 1):
                shutil.copy2(source_path, replica_path)
                log(f'Copied {source_path} to {replica_path}')

    for item in os.listdir(replica_folder):
        source_item = os.path.join(source_folder, item)
        replica_item = os.path.join(replica_folder, item)

        if not os.path.exists(source_item):
            if os.path.isdir(replica_item):
                shutil.rmtree(replica_item)
            else:
                os.remove(replica_item)
            log(f'Removed {replica_item}')

def log(message):
    with open(log_file_path, 'a') as log_file:
        log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} {message}\n')
    print(message)

while True:
    sync_folders(source_folder, replica_folder)
    log('Synchronized folders')
    time.sleep(interval)
