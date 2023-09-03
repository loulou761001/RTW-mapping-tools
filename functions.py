import re
from PIL import Image

# regex pattern for descr_regions.txt
RE_DESCR_REGIONS = re.compile(
    r"^(\w+)\n(?:^legion:\s+(\w+)\n)?(^\w+)\n(^\w+)\n(^\w+)\n(^\d+)\s+(\d+)\s+(\d+)\n(.+)\n(\d+)\n(\d+)\n?((?:\w+\s+\d+\s*)+)?^((\w+)\s+[0-9]+(\s)?)?+",
    re.M,
)

# this number must be high enough to cover the number of unique colors in map_regions.tga
MAX_COLORS = 10000


def remove_comments_and_empty_lines(text):
    """Remove empty lines, line-initial whitespace, and TW-style comments from `text`."""
    text = re.sub(r";.*", "", text, flags=re.M)
    text = re.sub(r"¬.*", "", text, flags=re.M)
    text = re.sub(r"[ \t]*$", "", text, flags=re.M)
    text = re.sub(r"^\s*", "", text, flags=re.M)
    return text


def tuple_to_string(tup, sep=" "):
    """Stringifies `tup` with the separator `sep` (default: space)."""
    return sep.join(map(str, tup))

# open map_regions.tga, get all unique colors, and convert colors to RGB strings
def colors_final():
    with Image.open("map_regions.tga") as im:
        im = im.convert("RGB")
        colors = im.getcolors(MAX_COLORS)
        colors_final = [tuple_to_string(color[1]) for color in colors]
        return colors_final


def is_not_negative(x):
    return x[0] >= 0 and x[1] >= 0

# from map_cropper import max_horiz, max_vert
def is_not_too_far(x):
    with Image.open("map_regions.tga") as im :
        max_vert = im.size[1]
        max_horiz = im.size[0]
        return x[0] <= max_horiz and x[1] <= max_vert

def filter_resources_coords(x):
    is_not_negative(x)
    is_not_too_far(x)

def parse_regions():
    with open("descr_regions.txt", "r", encoding="utf-8") as f:
        descr_regions = remove_comments_and_empty_lines(f.read())
        regions = []
        for match in RE_DESCR_REGIONS.findall(descr_regions):
            color = tuple(map(int, (match[5:8])))
            color = tuple_to_string(color)
            if color in colors_final():
                regions.append(
                    {
                        "name": match[0],
                        "legion": match[1],
                        "settlement": match[2],
                        "faction": match[3],
                        "rebel": match[4],
                        "color": tuple(map(int, (match[5:8]))),
                        "resources": match[8].strip(),
                        "triumph": int(match[9]),
                        "farm": int(match[10]),
                        "religion": match[11].strip(),
                    }
                )
    return regions