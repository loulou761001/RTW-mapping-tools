from PIL import Image

from functions import *


# prompt user
command = input(
    """- press 1 to regenerate descr_regions
- press 2 to regenerate all resources
- press 0 for all of the above
"""
).strip()

# validate input
if command not in ["0", "1", "2"]:
    raise TypeError("Sorry invalid input")
else:
    command = int(command)

if command in [0, 1]:
    print('Generating regions, please wait...')
    # parse regions from descr_regions.txt
    regions = list(parse_regions())

    # save a new descr_regions file containing only those regions whose colors remain on the cropped map_regions image
    with open("descr_regions_cropped.txt", "w", encoding="utf-8") as f:
        for region in regions:
            for key, value in region.items():
                if value:
                    if key == "name":
                        f.write(f"{value}\n")
                    elif key == "color":
                        f.write(f"\t{tuple_to_string(value)}\n")
                    elif key == "legion":
                        f.write(f"\tlegion: {value}\n")
                    else:
                        f.write(f"\t{value}\n")
            f.write("\n")

    # prompt user if they wish to generate in-game names for region tags
    generate_names = input("Generate names (y/n)? ").strip()
    if generate_names in ["y", "Y"]:
        print('Generating region names, please wait...')
        campaign_directory = input(
            "Enter the name of your campaign folder (default: imperial_campaign) --> "
        )
        if not campaign_directory.strip():
            campaign_directory = "imperial_campaign"
        else:
            campaign_directory = campaign_directory.strip().lower()

        # write new names file, accounting for the presence of legions and converting underscores to spaces
        new_names_file = campaign_directory + "_regions_and_settlement_names_cropped.txt"
        with open(new_names_file, "w", encoding="utf-16-le") as f:
            for region in regions:
                name = region["name"]
                name_text = " ".join(name.split("_"))
                settlement = region["settlement"]
                settlement_text = " ".join(settlement.split("_"))
                legion = region["legion"]
                legion_text = " ".join(legion.split("_"))

                f.write(f"{{{name}}}\t\t\t{name_text}\n")
                f.write(f"{{{settlement}}}\t\t\t{settlement_text}\n")
                if legion:
                    f.write(f"{{{legion}}}\t\t\t{legion_text}\n")

    print('Regions generated!')


if command in [0, 2] :
    # MOVE RESOURCES
    print('Generating resources, please wait...')
    with open("descr_strat_resources.txt", "r") as fr :
        descr_regions = remove_comments_and_empty_lines(fr.read())
    lines = descr_regions.split('\n')
    diffVert = input("Vertical difference (number of pixels) (see readMe) -->")
    # input validation
    if not diffVert.isnumeric() :
        raise TypeError("Sorry invalid input, expected a positive number")

    diffHor = input("Horizontal difference (number of pixels) -->")
    if not diffHor.isnumeric() :
        raise TypeError("Sorry invalid input, expected a positive number")
    diffVert = int(diffVert)
    diffHor = int(diffHor)
    #     diffVert = 144
    #     diffHor = 358
    with Image.open("map_regions.tga") as im :
        max_vert = im.size[1]
        max_horiz = im.size[0]
    coordsList = []
    for line in lines:
        if line.split():
            coords = [
                int(line.split(",")[2].strip()) - diffHor,
                int(line.split(",")[3].strip().split("\t")[0]) - diffVert,
                line.split(",")[1].strip(),
                line.split(",")[0].split("resource")[1].strip(),
            ]
            coordsList.append(coords)

    filteredCoords = list(filter(is_not_negative, coordsList))
    filteredCoords = list(filter(is_not_too_far, filteredCoords))

    # WRITE THE RESOURCES FILE
    newFileResources = open("descr_strat_resources_cropped.txt", "w")
    for coord in filteredCoords:
        newFileResources.write(
            "resource		"
            + coord[2]
            + ",              		"
            + coord[3]
            + ",			 "
            + str(coord[0])
            + ",  "
            + str(coord[1])
            + "\n"
        )
    print('Done!')
