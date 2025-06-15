from PIL import Image
import os

gif_path = "assets/confetti/confetti.gif"
output_folder = "assets/confetti/frames_trimmed"

os.makedirs(output_folder, exist_ok=True)

with Image.open(gif_path) as im:
    for i in range(im.n_frames):
        if i % 4 != 0:
            continue
        im.seek(i)
        frame = im.convert("RGBA")
        frame.save(f"{output_folder}/confetti_{i}.png")

print("Done: Trimmed frames exported.")
