import hashlib
import json
import os
import time

from loguru import logger
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

watch_path = R'D:\apps\XIVLauncherCN\Roaming\dalamudAssets'
watch_file = [
    'bannedplugin.json',
    'cheatplugin.json',
]
VALIDATOR = '6AD66461F0F582707E18C5F2AD99FF053B8BC9F9E1469848A660C00D34482F1AE9B513FBCB84DFD781F9DBBFC86DE1CD18268FFF07A61B3D6EBE6113D6E7EA5F'


def restore(file_path: str):
    time_to_stop = time.time() + 20
    while time.time() < time_to_stop:
        try:
            with open(file_path, 'r+', encoding='utf8') as f:
                content = json.load(f)
                # validate and handle files
                if len(content) == 0:
                    logger.warning(f'empty: {file_path}')
                    return
                if VALIDATOR.startswith(content[0]['Name']):
                    logger.debug(f'pass: {file_path}')
                    return
                # resotre contents
                for i in content:
                    i['Name'] = i['Name'] = hashlib.sha256(i['Name'].encode()).hexdigest().upper()[:len(i['Name'])]
                # add validator
                content[0]['Name'] = VALIDATOR[:len(content[0]['Name'])]
                # save
                f.seek(0)
                f.truncate()
                f.write(json.dumps(content, ensure_ascii=False, indent=2))
                logger.info(f'restored: {file_path}')
                return
        except Exception as e:
            logger.warning(f'{e}: {file_path}')
    logger.error(f'timed out: {file_path}')


class FileModifiedHandler(FileSystemEventHandler):
    def on_modified(self, event):
        filename = os.path.basename(event.src_path)
        if filename in watch_file:
            restore(event.src_path)


if __name__ == "__main__":
    def init_files():
        for root, _, files in os.walk(watch_path):
            for file in files:
                if file in watch_file:
                    restore(os.path.join(root, file))

    init_files()

    event_handler = FileModifiedHandler()
    observer = Observer()
    observer.schedule(event_handler, path=watch_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
