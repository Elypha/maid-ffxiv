import os
import time

import cv2
import maid.funcs as funcs
import maid.logging_debug as logging
import maid.window_ffxiv as window_ffxiv
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

LANG     = conf['main']['lang']

IS_LOOP  = conf['main']['retainer']['is_loop']
GAP      = conf['main']['retainer']['gap']
POS_TALK = tuple(conf['client'][LANG]['pos_talk'])

logger.warning(F"Lang: {LANG}")
logger.warning(F"Loop: {IS_LOOP}")
logger.warning(F"Gap:  {GAP}")

# init
IMG_LIST      = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_list.png")
IMG_COMPLETED = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_completed.png")
IMG_TALK      = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\npc_talk_normal.png")
IMG_COMPLETE  = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_complete.png")
IMG_REASSIGN  = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_reassign.png")
IMG_ASSIGN    = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_assign.png")
IMG_QUIT      = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\guyuan_quit.png")

ffxiv = window_ffxiv.FFXIV(
    handle=funcs.get_hwnd(conf['main']['title']),
    content_size=conf['main']['content_size'],
    window_offset=conf['main']['window_offset'],
    capture_mod=conf['main']['capture_mod'],
    is_client_area=conf['main']['is_client_area'],
    conf=conf,
    cache=cache
)


@logger.catch
def main_loop():
    global count

    while True:
        # 等待雇员列表
        ffxiv.mouse_moveTo((3150, 450))
        logger.trace('Waiting for retainer list.')
        ffxiv.find_image_loop(IMG_LIST, (1250, 800), (150, 150))
        # 检查是否有结束
        c, pos = ffxiv.find_image(IMG_COMPLETED, (2040, 570), (160, 260))
        if c > 0.95:
            count += 1
            logger.info(F'Completed: {count}')
            # 点击结束
            ffxiv.mouse_moveTo((pos[0], pos[1] + 5))
            ffxiv.mouse_L()
            # 点击对话框
            ffxiv.find_image_loop(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
            ffxiv.mouse_L()
            # 点击结束
            c, pos = ffxiv.find_image_loop(IMG_COMPLETE, (1610, 650), (200, 100))
            ffxiv.mouse_moveTo((pos[0], pos[1] + 5))
            ffxiv.mouse_L()
            # 重新委托
            c, pos = ffxiv.find_image_loop(IMG_REASSIGN, (1580, 750), (200, 100))
            ffxiv.mouse_moveTo((pos[0], pos[1] + 5))
            ffxiv.mouse_L()
            # 委托
            time.sleep(0.2)
            c, pos = ffxiv.find_image_loop(IMG_ASSIGN, (1540, 820), (200, 100), threshold=0.99)
            ffxiv.mouse_moveTo((pos[0], pos[1] + 5))
            ffxiv.mouse_L()
            # 点击对话框
            ffxiv.find_image_loop(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
            ffxiv.mouse_L()
            # 返回
            c, pos = ffxiv.find_image_loop(IMG_QUIT, (1520, 800), (200, 100))
            ffxiv.mouse_moveTo((pos[0] + 20, pos[1] + 5))
            ffxiv.mouse_L()
            # 点击对话框
            ffxiv.find_image_loop(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
            ffxiv.mouse_L()
        else:
            logger.warning('Nothing to complete.')
            ffxiv.key_press('esc')
            return


def main():
    global count

    count = 0
    while True:
        ffxiv.to_foreground()

        ffxiv.key_press('numpad_0')
        ffxiv.key_press('numpad_0')
        ffxiv.key_press('numpad_0')

        main_loop()

        if IS_LOOP == 0:
            return

        logger.success(f'Wait {GAP} seconds ...')
        time.sleep(GAP)


main()
