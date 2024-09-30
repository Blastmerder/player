import dearpygui.dearpygui as dpg
import music_tag
from PIL import Image, ImageEnhance
import io
import numpy as np


class Track:
    def __init__(self, *, path, texture_reg, background: Image):
        self.path = path
        self._texture_reg = texture_reg
        self._background = background

        self._f = music_tag.load_file(path)

        self.author = self._f.resolve('album artist')
        self.title = self._f.resolve('title')
        self._texture_id = None

    @property
    def texture_id(self):
        if self._texture_id is None:
            self._draw()
        return self._texture_id

    def _draw(self):
        artwork = self._f['artwork']
        artwork_data = artwork.first.data
        if artwork_data is not None:
            im = io.BytesIO(artwork_data)
            self.imageFile = Image.open(im)
            trash = (self.imageFile.size[0] - self.imageFile.size[1]) // 2
            self.imageFile = self.imageFile.crop((trash, 0, self.imageFile.size[0] - trash, self.imageFile.size[1]))

            image_mask = Image.open(r'textures/mask.png')
            image_mask = image_mask.resize((self.imageFile.size[0], self.imageFile.size[1]))

            layer = Image.new("RGBA", self.imageFile.size, 0)
            mask_layer = Image.new("L", self.imageFile.size, 0)
            mask_layer.paste(image_mask)

            background = self._background.resize(self.imageFile.size)
            layer.paste(background)
            layer.paste(self.imageFile, None, mask_layer)
        else:
            layer = self._background
            self.imageFile = self._background

        self.multiplier_size = 230 / max(layer.size[0], layer.size[1])
        layer = layer.resize((
            int(layer.size[0] * self.multiplier_size),
            int(layer.size[1] * self.multiplier_size)
        ))

        image_data = np.array(layer.convert("RGBA")).flatten() / 255
        self._texture_id = dpg.add_static_texture(
            layer.size[0],
            layer.size[1],
            image_data,
            parent=self._texture_reg
        )

