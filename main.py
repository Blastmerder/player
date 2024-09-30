import dearpygui.dearpygui as dpg
import DearPyGui_DragAndDrop as dpg_dnd
import time
from pygame import mixer
import music_tag
import os
from pydub import AudioSegment
from PIL import Image, ImageEnhance
import io
import numpy as np

from Moduls.track import Track


dpg.create_context()
dpg_dnd.initialize()
dpg.create_viewport(
    title="Drag and drop example",
    width=600,
    height=600,
    small_icon=r'textures\player.ico',
    large_icon=r'textures\player.ico'
)


dpg.setup_dearpygui()
dpg.show_viewport()


class Player:
    def __init__(self):
        self.playlist: list[Track] = []

        self.texture_reg = dpg.add_texture_registry()
        self.background = Image.open(r'textures/vinil.png')

        with dpg.window(no_scrollbar=True, no_scroll_with_mouse=True) as self.main_window:
            with dpg.child_window() as self.data_window:
                ...
            with dpg.child_window() as self.artwork_window:
                ...
            with dpg.child_window() as self.timeline_window:
                ...
        dpg.set_primary_window(self.main_window, True)

        with dpg.viewport_menu_bar() as self.bar:
            dpg.add_button(label='aaa', callback=lambda: print(11))

        dpg_dnd.set_drop(self.drop)

    def drop(self, data, keys):
        print(f'{data}')
        print(f'{keys}')

        for path in data:
            if os.path.isfile(path) and path.split('.')[-1] == 'mp3':
                self.playlist.append(Track(path=path, texture_reg=self.texture_reg, background=self.background))

        iamge = dpg.add_image(self.playlist[-1].texture_id, parent=self.artwork_window)

        """
        mixer.init()
        mixer.music.load(data[0])
        mixer.music.play()
        mixer.music.set_volume(0)
        while mixer.music.get_busy():  # wait for music to finish playing

            time.sleep(1)"""

    @staticmethod
    def __set_pos_scale(pos: tuple[int, int], scale: tuple[int, int], window):
        dpg.set_item_width(window, scale[0])
        dpg.set_item_height(window, scale[1])

        dpg.set_item_pos(
            window,
            [
                pos[0],
                pos[1]
            ]
        )

    def update(self):
        global_height = dpg.get_item_height(self.main_window)
        global_width = dpg.get_item_width(self.main_window)

        self.__set_pos_scale(
            (
                8,
                global_height - dpg.get_item_height(self.artwork_window) - 8
            ),
            (250, 250),
            self.artwork_window
        )

        self.__set_pos_scale(
            (8, 5),
            (250, global_height - 13 - dpg.get_item_height(self.artwork_window)),
            self.data_window
        )

        self.__set_pos_scale(
            (258, global_height-dpg.get_item_height(self.timeline_window) - 8),
            (global_width-266, 50),
            self.timeline_window
        )


player = Player()


while dpg.is_dearpygui_running():
    player.update()
    dpg.render_dearpygui_frame()
dpg.destroy_context()
