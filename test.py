import os
import time

import cv2
import maid.funcs as funcs
import maid.window_ffxiv as window_ffxiv
import tomlkit
from line_profiler import LineProfiler

# THIS_DIR = R'D:\JK Auto'
THIS_DIR = os.path.split(os.path.realpath(__file__))[0]


# read config
with open(fR'{THIS_DIR}/config.toml', 'r', encoding='utf8') as f:
    conf = tomlkit.load(f)

with open(fR'{THIS_DIR}/JK_Crafting.toml', 'r', encoding='utf8') as f:
    cache = tomlkit.load(f)

LANG = conf['main']['lang']

WHITE_PIXEL_POS = tuple(conf['client'][LANG]['white_pixel_pos'])
WHITE_PIXEL_RGB = tuple(conf['client'][LANG]['white_pixel_rgb'])


ffxiv = window_ffxiv.FFXIV(
    # handle=331862,
    handle=funcs.get_hwnd(conf['main']['title']),
    client_area_size=conf['main']['client_area_size'],
    bar_offset=conf['main']['bar_offset'],
    window_offset=conf['main']['window_offset'],
    capture_mod=conf['main']['capture_mod'],
    is_client_area=True,
    conf=conf,
    cache=cache
)

# image = ffxiv.capture((0, 0), (3440, 1392))
image = ffxiv.capture_BitBlt((0, 0), (3440, 1392))
cv2.imwrite('test.png', image)

# ------------------------
# import time

# LOOP=100
# t0 = time.time()
# for i in range(LOOP):
#     ffxiv.capture_BitBlt((0, 0), (3440, 1392))
#     # ffxiv.capture((0, 0), (3440, 1392))
# print(f"Time: {(time.time() - t0) / LOOP}")
