import os
import winsound

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

LANG = conf['main']['lang']

POS_TALK = tuple(conf['client'][LANG]['pos_talk'])

# init
IMG_TALK         = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\npc_talk_normal.png")
IMG_86           = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\leaves_lvl86.png")
IMG_LEVE         = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\leaves_lvl86_jujiang.png")
IMG_RECEIVE      = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\leaves_receive.png")
IMG_LEVE_FINISH  = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\leve_craft_finish.png")


ffxiv = window_ffxiv.FFXIV(
    handle=funcs.get_hwnd(conf['main']['title']),
    client_area_size=conf['main']['client_area_size'],
    bar_offset=conf['main']['bar_offset'],
    window_offset=conf['main']['window_offset'],
    capture_mod=conf['main']['capture_mod'],
    conf=conf,
    cache=cache
)


@logger.catch
def main_loop():
    global count

    # 点击对话框
    logger.trace('点击对话框')
    ffxiv.find_image_loop(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
    ffxiv.key_press('numpad_0')
    # 选2制作
    ffxiv.key_press('2')
    # 选86级
    logger.trace('选86级')
    _, pos = ffxiv.find_image_loop(IMG_86, (155, 275), (80, 80))
    ffxiv.mouse_moveTo((pos[0], pos[1]))
    ffxiv.mouse_L()
    # 选巨匠理符
    logger.trace('选巨匠理符')
    _, pos = ffxiv.find_image_loop(IMG_LEVE, (181, 284), (300, 110))
    ffxiv.mouse_moveTo((pos[0], pos[1]))
    ffxiv.mouse_L()
    # 选接受
    logger.trace('选接受')
    _, pos = ffxiv.find_image_loop(IMG_RECEIVE, (661, 623), (80, 40))
    ffxiv.mouse_moveTo((pos[0], pos[1]))
    ffxiv.mouse_L()
    # 等待接受完成
    logger.trace('等待接受完成')
    c = 1
    while c > 0.9:
        c, _ = ffxiv.find_image(IMG_LEVE, (181, 284), (300, 110))
        logger.trace(f'c: {c}')
    # 关闭对话框
    ffxiv.key_press('esc')
    ffxiv.key_press('esc')
    ffxiv.key_press('decimal_key')
    ffxiv.key_press('decimal_key')
    ffxiv.key_press('decimal_key')
    ffxiv.key_press('decimal_key')

    # 交理符
    ffxiv.mouse_moveTo((1960, 840))
    ffxiv.mouse_R()
    # 点击对话框
    logger.trace('点击对话框')
    ffxiv.find_image_loop(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
    ffxiv.key_press('numpad_0')
    # 交巨匠
    logger.trace('交巨匠')
    c = 0
    while c < 0.8:
        ffxiv.key_press('numpad_0')
        c, _ = ffxiv.find_image(IMG_LEVE_FINISH, (1585, 150), (100, 40))
        logger.trace(f'c: {c}')
    logger.trace('交完')
    ffxiv.key_press('numpad_0')
    ffxiv.key_press('numpad_0')

    # 接
    ffxiv.mouse_moveTo((1440, 840))

    logger.trace('等待idle')
    ffxiv.wait_idle()
    logger.trace('idle完成')
    ffxiv.mouse_R()


def main():
    global count

    count = 0
    winsound.Beep(1000, 100)
    winsound.Beep(1000, 100)

    while True:
        main_loop()
        count += 1
        logger.info(f'count: {count}')


main()
