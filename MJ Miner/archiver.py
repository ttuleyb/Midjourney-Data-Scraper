from pathlib import Path
import os
from datetime import datetime
paths = Path("jsons").glob("*.json")

if len(os. listdir('jsons')) < 1:
    print("No files found exiting...")
else:

    today = datetime.today().strftime('%Y-%m-%d')

    #Move all files to a folder with date as its name
    if not os.path.exists("jsons\\" + today):
        os.makedirs("jsons\\" + today)

    for i in paths:
        filePath = "jsons\\" + i.name
        os.rename(filePath, "jsons\\" + today + "\\" + i.name)
        print(filePath)

    #Add all new data to the db
    import mongoshenenigans

    #Move all folders to an archive
    if not os.path.exists("archive"):
        os.makedirs("archive")

    for folder in os.listdir("jsons"):
        folderLocation = os.path.join("jsons", folder)
        if os.path.isdir(folderLocation):
            print(folder)
            os.rename(folderLocation, "archive\\" + folder)