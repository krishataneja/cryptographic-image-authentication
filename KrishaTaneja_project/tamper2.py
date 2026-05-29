from PIL import Image, ImageDraw, PngImagePlugin

img = Image.open("testt_signed.png")

metadata = PngImagePlugin.PngInfo()
for key, value in img.info.items():
    if isinstance(value, str):  
        metadata.add_text(key, value)

draw = ImageDraw.Draw(img)
draw.point((10, 10), fill=(255, 0, 0))


img.save("testt_tampered.png", "PNG", pnginfo=metadata)

print("Created tampered image with signature intact")