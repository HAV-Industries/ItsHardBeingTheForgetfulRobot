# /// script
# dependencies = [
#     "cffi",
#     "raylib"
# ]
# ///
import asyncio
import platform
from pyray import *


async def main():
    init_window(500, 500, "Hello")
    platform.window.window_resize()
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        draw_text("Vaed drilltool", 190, 200, 20, VIOLET)
        end_drawing()
        await asyncio.sleep(0)
    close_window()


asyncio.run(main())
