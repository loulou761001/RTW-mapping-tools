from PIL import Image, ImageTk
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
import string

from functions import *
print("Loading, please wait...")

colorsFinal = colors_final()


# parse regions from descr_regions.txt
regions = list(parse_regions())

# --------------------------------------

def on_click(event):
    print("image clicked, please wait...")
    color = map_regions.getpixel((event.x, event.y))
    if color in [(255,255,255),(0,0,0),(41,140,233)] :
        raise TypeError("Invalid pixel, please do not select a water, city or port pixel.")
    print(color,(event.x, event.y))
    current_region = []
    for i, region in enumerate(regions) :
        if tuple_to_string(region['color']).strip() == str(color[0])+' '+str(color[1])+' '+str(color[2]) :
            current_region = region
            break

    if current_region :
        print("region selected : ",current_region['name'])
        print('details : \n',current_region)

        region = input("Enter the region's new name ("+current_region['name'].strip()+") : ")
        if not region.strip() : region = current_region['name']
        else : region = str(region.strip().replace(' ', '_'))
        current_region['name'] = region
        print(current_region['name'])

        legion = input("Enter the region's new legion name (optional) ("+current_region['legion'].strip()+") : ")
        if not legion.strip() : legion = current_region['legion']
        else : legion = str(legion.strip().replace(' ', '_'))
        print(legion)
        current_region['legion'] = legion

        settlement = input("Enter the region's new settlement name ("+current_region['settlement'].strip()+") : ")
        if not settlement.strip() : settlement = current_region['settlement']
        else : settlement = str(settlement.strip().replace(' ', '_'))
        print(settlement)
        current_region['settlement'] = settlement

        faction = input("Enter the region's original faction/culture ("+current_region['faction'].strip()+") : ")
        if not faction.strip() : faction = current_region['faction']
        else : faction = str(faction.strip().replace(' ', '_'))
        print(faction)
        current_region['faction'] = faction

        rebels = input("Enter the region's new rebels ("+current_region['rebel'].strip()+") : ")
        if not rebels.strip() : rebels = current_region['rebel']
        else : rebels = str(rebels.strip().replace(' ', '_'))
        print(rebels)
        current_region['rebel'] = rebels

        resources = input("Enter the region's resources as a comma-separated resources list ("+current_region['resources'].strip()+") : ")
        if not resources.strip() : resources = current_region['resources']
        else : resources = str(resources.strip())
        if not re.match(r'^(\w+)(,\s\w+)*$',resources):
            raise TypeError("Sorry invalid input, expected a comma separated list (x, y, z, ...)")
        print(resources)
        current_region['resources'] = resources

        triumph = input("Enter the region's triumph points value ("+str(current_region['triumph']).strip()+") : ")
        if not triumph.strip() : triumph = current_region['triumph']
        else : triumph = str(triumph.strip())
        print(triumph)
        if not str(triumph).isnumeric():
            raise TypeError("Sorry invalid input, expected a positive number")
        current_region['triumph'] = triumph

        farmLevel = input("Enter the region's base farm level ("+str(current_region['farm']).strip()+") : ")
        if not farmLevel.strip() : farmLevel = current_region['farm']
        else : farmLevel = str(farmLevel.strip())
        print(farmLevel)
        if not str(farmLevel).isnumeric():
            raise TypeError("Sorry invalid input, expected a positive number")
        current_region['farm'] = farmLevel

        # if current_region['religion'].strip() :
        religion = input("Enter the region's religion(s) (optional) (the percentages must add up to 100) ("+current_region['religion'].strip()+") : ")
        if not religion.strip() : religion = current_region['religion']
        else : religion = str(religion.strip().replace(' ', '_'))
        if religion.strip() and not re.match(r'^(\w+\s\d(\d)?)(\s\w+\s\d(\d)?)*$', religion.strip()):
            raise TypeError("Sorry invalid input, wrong format (name percentage name percentage...)")
        print(religion)
        current_region['religion'] = religion
        regions[i] = current_region
        print(regions[i])

        campaign_directory = input(
            "Enter the name of your campaign folder (default: imperial_campaign) --> "
        )
        if not campaign_directory.strip():
            campaign_directory = "imperial_campaign"
        else:
            campaign_directory = campaign_directory.strip().lower()
        newNamesFile = open(campaign_directory+'_regions_and_settlement_names_new.txt','w')
        
        print('Writing '+campaign_directory+'_regions_and_settlement_names_new...')
        for region in regions :
            newNamesFile.write('{'+region['name'].strip()+'}			'+region['name'].strip().replace('_',' ')+'\n')
            newNamesFile.write('{'+region['settlement'].strip()+'}			'+region['settlement'].strip().replace('_',' ')+'\n')
        print('Names created!')
        
        print('Writing descr_regions_new...')
        with open('descr_regions_new.txt', 'w') as f:
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
        print('Done!\n\n\n')
        
        
        
with Image.open("map_regions.tga") as map_regions :
    map_regions = map_regions.resize((map_regions.width*3, map_regions.height*3), Image.NEAREST)
    root = tk.Tk()
    photo = ImageTk.PhotoImage(map_regions)
    l = tk.Label(root, image=photo)
    l.pack()
    l.bind('<Button-1>', on_click)
    print("Loaded! please click a region on the map.")


    root.mainloop()

