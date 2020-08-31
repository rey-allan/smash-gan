import numpy as np
import torchvision.transforms.functional as TF

from pathlib import Path
from PIL import Image


class PathProvider:
    def __init__(self, character):
        self._character = character
        self._index = 0

        # Create the folder for the character
        self._root = Path(f'data/{character}')
        self._root.mkdir(exist_ok=True)

    def get(self):
        p = self._root.joinpath(f'{self._character}{self._index + 1}.png')
        self._index += 1

        return p

# DCGAN works best with 64 x 64 images
image_size = 64

transforms = [
    (TF.adjust_brightness, 'brightness_factor', np.linspace(0.5, 2.0, num=8)),
    (TF.adjust_gamma, 'gamma', np.linspace(0.5, 2.0, num=8)),
    (TF.adjust_hue, 'hue_factor', np.linspace(-0.5, 0.5, num=10)),
    (TF.rotate, 'angle', np.linspace(-45, 45, num=40))
]


if __name__ == '__main__':
    # Go through all the original images
    # We assume the directory follows the structure as created by `download_characters.py`
    for character_folder in Path('./original').iterdir():
        if character_folder.stem.startswith('.'):
            continue

        print(f'Processing character: {character_folder.stem}')
        path = PathProvider(character_folder.stem)

        for skin in character_folder.iterdir():
            if skin.stem.startswith('.'):
                continue

            with open(skin, 'rb') as f:
                img = Image.open(f)
                
                # Resize the original image
                img = TF.resize(img, (image_size, image_size))
                img.save(path.get())

                # Flip it
                i = TF.hflip(img)
                i.save(path.get())

                # Augment using all the other transformations plus also flip them as well
                for (t, param, values) in transforms:
                    for v in values:
                        i = t(img, **{param: v})
                        i.save(path.get())

                        i = TF.hflip(i)
                        i.save(path.get())
