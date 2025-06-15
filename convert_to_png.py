from PIL import Image
import os

gif_path = "assets/money/money.gif"
output_folder = "assets/money/money_trimmed"

os.makedirs(output_folder, exist_ok=True)

with Image.open(gif_path) as im:
    for i in range(im.n_frames):
        im.seek(i)
        frame = im.convert("RGBA")
        frame.save(f"{output_folder}/money_{i}.png")

print("Done: All frames exported.")
