from PIL import Image

from functions import *


# prompt user
print('This file will generate the slave resource for all of your regions. The resource will be placed on the settlements.')



# DECLARE SLAVES
print('Generating slaves, please wait...')
with Image.open("map_regions_flipped.tga") as map_regions_flipped :
    found_pixels = []
    for i, pixel in enumerate(map_regions_flipped.getdata()):
        if pixel == (0, 0, 0):
            width, height = map_regions_flipped.size
            # Get pixel coords with index and image width
            x, y = divmod(i, width)
            found_pixels.append((x, y))
with open("descr_strat_slaves_new.txt", "w") as f:
    f.write(";;slaves\n")
    for slave in found_pixels:
        f.write(
            "resource		slaves,             		1,			 "
            + str(slave[0])
            + ", "
            + str(slave[1])
            + "\n"
        )
print('Done!')

