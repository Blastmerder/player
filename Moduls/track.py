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


class Track:
    def __init__(self, *, path, texture_reg, background: Image):
        self.path = path

        f = music_tag.load_file(path)

        artwork = f['artwork']
        artwork_data = artwork.first.data
        if artwork_data is not None:
            im = io.BytesIO(artwork_data)
            self.imageFile = Image.open(im)

            image_mask = Image.open(r'textures/mask.png')
            image_mask = image_mask.resize((artwork.first.width, artwork.first.height))

            layer = Image.new("RGBA", self.imageFile.size, 0)
            mask_layer = Image.new("L", self.imageFile.size, 0)
            mask_layer.paste(image_mask)

            background = background.resize(self.imageFile.size)
            layer.paste(background)
            layer.paste(self.imageFile, None, mask_layer)
        else:
            layer = background
            self.imageFile = background

        self.multiplier_size = 230 / max(layer.size[0], layer.size[1])
        layer = layer.resize((
            int(layer.size[0] * self.multiplier_size),
            int(layer.size[1] * self.multiplier_size)
        ))
        print(layer.size[0])

        image_data = np.array(layer.convert("RGBA")).flatten() / 255
        self._texture_id = dpg.add_static_texture(
            layer.size[0],
            layer.size[1],
            image_data,
            parent=texture_reg
        )

    @property
    def texture_id(self):
        return self._texture_id
