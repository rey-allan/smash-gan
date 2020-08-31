import requests
import shutil
import time

from pathlib import Path
from PIL import Image


# Mii Fighter wasn't considered because the images had the names on them which could confuse the algorithm
characters = [
    "mario", "donkey_kong", "link", "samus", "dark_samus", "yoshi", "kirby", "fox", "pikachu", "luigi", "ness", "captain_falcon",
    "jigglypuff", "peach", "daisy", "bowser", "ice_climbers", "sheik", "zelda", "dr_mario", "pichu", "falco", "marth", "lucina",
    "young_link", "ganondorf", "mewtwo", "roy", "chrom", "mr_game_and_watch", "meta_knight", "pit", "dark_pit", "zero_suit_samus", "wario", "snake",
    "ike", "pokemon_trainer", "diddy_kong", "lucas", "sonic", "king_dedede", "olimar", "lucario", "rob", "toon_link", "wolf", "villager",
    "mega_man", "wii_fit_trainer", "rosalina_and_luma", "little_mac", "greninja", "palutena", "pac_man", "robin", "shulk", "bowser_jr",
    "duck_hunt", "ryu", "ken", "cloud", "corrin", "bayonetta", "inkling", "ridley", "simon", "richter", "king_k_rool", "isabelle", "incineroar",
    "piranha_plant", "joker", "dq_hero", "banjo_and_kazooie", "terry", "byleth", "minmin"
]

base_url = 'https://www.smashbros.com/assets_v2/img/fighter/{character}/main{skin}.png'


if __name__ == '__main__':
    print(f'Downloading images for {len(characters)} characters')
    failed = []

    for character in characters:
        print(f'Downloading: {character}')

        # Create the subdirectory for each character
        folder = Path(f'original/{character}')
        folder.mkdir(exist_ok=True)
    
        for skin in range(0, 8):
            # Define the skin based on the format used by Nintendo
            skin = str(skin + 1) if skin != 0 else ''
            # Define the path where the images will be stored
            path = folder.joinpath(f'{character}{skin}.png')

            # Check for existence to allow resuming the script
            if Path(path).exists():
                continue

            url = base_url.format(character=character, skin=skin)
            r = requests.get(url, stream=True)

            if r.status_code == 200:
                with open(path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            else:
                failed.append(url)

            # Convert to RGB with a black background
            # We can't really work with transparent images
            with open(path, 'rb') as f:
                img = Image.open(f)
                img.convert("RGBA")

                # Create a black image
                new_img = Image.new('RGBA', img.size, (0, 0, 0, 255))
                # Paste the original image into this new black background using the alpha channel as mask
                new_img.paste(img, mask=img.split()[-1])

                # Save the image as RGB
                new_img.convert('RGB').save(path)

        time.sleep(.1)

    if failed:
        print(f'The following {len(failed)} character images failed to download: {failed}')
