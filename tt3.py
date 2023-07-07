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

LANG          = conf['main']['lang']

IS_LOOP       = conf['main']['retainer']['is_loop']
GAP           = conf['main']['retainer']['gap']
POS_TALK      = tuple(conf['client'][LANG]['pos_talk'])

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
    client_area_size=conf['main']['client_area_size'],
    bar_offset=conf['main']['bar_offset'],
    window_offset=conf['main']['window_offset'],
    capture_mod=conf['main']['capture_mod'],
    is_client_area=True,
    conf=conf,
    cache=cache
)


# while True:
#     t0 = time.time()
#     c, pos = ffxiv.find_image(IMG_TALK, (POS_TALK[0], POS_TALK[1]), (POS_TALK[2], POS_TALK[3]))
#     logger.debug(F"Talk: {c} {pos}, {time.time() - t0:.5f}")
IMG_LEVE_FINISH  = cv2.imread(RF"{THIS_DIR}\assets\{LANG}\leve_craft_finish.png")

c, _ = ffxiv.find_image(IMG_LEVE_FINISH, (1585, 150), (100, 40))

print(c)
