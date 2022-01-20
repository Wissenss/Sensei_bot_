'''from PIL import Image
import os

for file in os.listdir("assets/cards"):
    print(file)

image_1 = Image.open("assets/cards/Card-Jitsu_Cards_full_1.png")
image_1.show()'''

from PIL import Image

images = [Image.open(x) for x in ['assets/cards/Card-Jitsu_Cards_full_2.png', 'assets/cards/Card-Jitsu_Cards_full_2.png', 'assets/cards/Card-Jitsu_Cards_full_3.png']]
widths, heights = zip(*(i.size for i in images))

total_width = sum(widths)
max_height = max(heights)

new_im = Image.new('RGB', (total_width, max_height))

x_offset = 0
for im in images:
    new_im.paste(im, (x_offset,0))
    x_offset += im.size[0]

new_im.save('assets/test.jpg')