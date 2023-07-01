import os
import re
import time

import cv2
import maid.funcs as funcs
import maid.logging_debug as logging
import numpy
import tomlkit

# THIS_DIR = R'D:\JK Maid\FFXIV'
THIS_DIR = os.path.split(os.path.realpath(__file__))[0]


# logging
logger = logging.logger


# read config
logger.debug(F'Config: {THIS_DIR}\config.toml')
with open(fR'{THIS_DIR}/config.toml', 'r', encoding='utf8') as f:
    conf = tomlkit.load(f)

logger.debug(F'Cache: {THIS_DIR}\cache.toml')
with open(fR'{THIS_DIR}/JK_Crafting.toml', 'r', encoding='utf8') as f:
    cache = tomlkit.load(f)

LANG            = conf['main']['lang']

WHITE_PIXEL_POS = tuple(conf['client'][LANG]['white_pixel_pos'])
WHITE_PIXEL_RGB = tuple(conf['client'][LANG]['white_pixel_rgb'])
IS_TRIAL        = cache['main']['is_trial']
TOTAL_CRAFTS    = cache['main']['total_crafts']
TIME_LIMIT      = cache['main']['time_limit']
DELAY           = cache['main']['delay']
IS_NOTIFICATION = cache['main']['is_notification']
IS_BACKGROUND   = cache['main']['is_background']

logger.warning(f'语言 = {LANG}')
logger.warning(f'制作练习 = {IS_TRIAL}')
logger.warning(f'次数 = {TOTAL_CRAFTS}')
if TIME_LIMIT > 0:
    TIME_TO_STOP = time.time() + TIME_LIMIT * 60
    logger.warning(f'时间限制 = {TIME_LIMIT} min')
else:
    TIME_TO_STOP = 0


# read recipe
logger.debug('Read recipe')
with open(fR'{THIS_DIR}\JK_Crafting_recipe.txt', 'r', encoding='utf8') as f:
    recipe = re.sub(
        r'^(?P<indent> *)(?P<skill>[^#\s]+?)\((?P<count>\d+)\)$',
        R"\g<indent>ffxiv.craft('\g<skill>', \g<count>)",
        f.read().strip(),
        flags=re.MULTILINE
    )
recipe_title = re.match(r'^#(?P<title>.+?)$', recipe, flags=re.MULTILINE).group('title')
logger.warning(F"配方 = {recipe_title.strip()}")


# init
logger.debug('Init...')
IMG_CRAFTING_NOTE  = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_note.png')
IMG_CRAFTING_PANEL = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_panel.png')
IMG_Q_NORMAL       = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_status_normal.png')
IMG_Q_HIGH         = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_status_high.png')
IMG_Q_MAX          = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_status_max.png')
IMG_Q_LOW          = cv2.imread(fR'{THIS_DIR}\assets\{LANG}\crafting_status_low.png')

ffxiv = funcs.FFXIV(
    handle=funcs.get_hwnd('ffxiv', LANG),
    client_area_size=conf['main']['client_area_size'],
    bar_offset=conf['main']['bar_offset'],
    window_offset=conf['main']['window_offset'],
    capture_mod=conf['main']['capture_mod'],
    conf=conf,
    cache=cache
)
logger.success('Done\n')


# start delay
while DELAY > 0:
    print(F'Starting in {DELAY:.1f} seconds ...    \r', end='')
    time.sleep(0.1)
    DELAY = DELAY - 0.1


def is_crafting_panel():
    c, _ = ffxiv.find_image(IMG_CRAFTING_PANEL)
    if c > 0.98:
        return True
    else:
        return False


def Q():
    ffxiv.wait_idle()
    pos_start = (panel_pos[0] + 10, panel_pos[1] + 15)
    rect = (64, 21)
    # 通常
    c1, _ = ffxiv.find_image(IMG_Q_NORMAL, pos_start, rect)
    if c1 > 0.98:
        return 1
    # 高品质
    c2, _ = ffxiv.find_image(IMG_Q_HIGH, pos_start, rect)
    if c2 > 0.98:
        return 2
    # 最高品质
    c3, _ = ffxiv.find_image(IMG_Q_MAX, pos_start, rect)
    if c3 > 0.98:
        return 3
    # 低品质
    c4, _ = ffxiv.find_image(IMG_Q_LOW, pos_start, rect)
    if c4 > 0.98:
        return 0


def main_loop():
    global panel_pos

    # locate crafting note
    _, note_pos = ffxiv.find_image_loop(IMG_CRAFTING_NOTE)

    # try to open crafting panel
    if IS_BACKGROUND:
        retries = 0
        while not is_crafting_panel():
            retries += 1
            if retries > 100:
                logger.error('Failed to open crafting panel. Too many retries.')
                quit()
            ffxiv.key_press('numpad_0')
            ffxiv.key_press('numpad_0')
            time.sleep(0.3)
    else:
        ffxiv.to_foreground()
        if IS_TRIAL == 1:
            # trial craft
            pos_craft = (note_pos[0] + 511, note_pos[1] + 519)
        else:
            # real craft
            pos_craft = (note_pos[0] + 777, note_pos[1] + 520)
        ffxiv.mouse_moveTo(pos_craft)
        ffxiv.mouse_L()

    # double check crafting panel is open
    while True:
        c, panel_pos = ffxiv.find_image(IMG_CRAFTING_PANEL)
        if c > 0.98:
            break
        if IS_BACKGROUND:
            ffxiv.key_press('numpad_0')
    if not is_crafting_panel():
        logger.error('未能打开制作面板 -> 退出')
        quit()

    exec(recipe)


def main():
    # init
    c_crafts = 0
    time_all_crafts = []
    time_start = time.time()
    if TOTAL_CRAFTS > 0:
        digits_len = len(str(TOTAL_CRAFTS))
    else:
        digits_len = 3
    time_last = None

    # loop
    while True:
        main_loop()
        c_crafts += 1
        time_now = time.time()
        # generate report
        if time_last:
            # 2+ crafts
            time_all_crafts.append(time_now - time_last)
            time_all_crafts_avg = numpy.mean(time_all_crafts)
            time_to_finish = time.strftime(
                '%H:%M:%S',
                time.localtime(time_now + (TOTAL_CRAFTS - c_crafts) * time_all_crafts_avg)
            )
            logger.info(F'第 {c_crafts:>{digits_len}} / {TOTAL_CRAFTS} 次完成！用时 {time_all_crafts[-1]:.2f} ({time_all_crafts_avg:.2f}) 秒')
            print(F'  >> 预期: {time_to_finish}\r', end='')
        else:
            # 1st craft
            os.system('cls')
            logger.info(F'第 {c_crafts:>{digits_len}} / {TOTAL_CRAFTS} 次完成！')

        time_last = time_now
        # check crafts limit
        if (c_crafts >= TOTAL_CRAFTS) and (TOTAL_CRAFTS != 0):
            logger.warning('-- 达到指定次数 --')
            break
        time_spent = time_now - time_start
        if TIME_TO_STOP and (time_spent > TIME_TO_STOP):
            logger.warning('-- 达到指定时间 --')
            break

    logger.success('工作结束')
    logger.success(F'共计 {c_crafts} 次，用时 {time_spent//60:.0f} 分 {time_spent%60:.2f} 秒。')


main()
