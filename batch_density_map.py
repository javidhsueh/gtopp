import density_map
import os
from multiprocessing import Process

INPUT_FILE = ["BlueShark", "CommonThresherShark", "JuvenileWhiteShark", "SalmonShark", "WhiteShark"]

# run each algorithm several times and logged to folders
for file_name in INPUT_FILE:
    file_fullpath = "./data/" + file_name + ".json"
    args = []
    args.append("-i=" + file_fullpath)

    dest_fullpath = "./result/" + file_name+"/"

    args.append("-o="+dest_fullpath)

    # if not os.path.exists(dest_fullpath):
    os.makedirs(dest_fullpath)

    # density_map.main(args)
    p = Process(target=density_map.main, args=(args,))
    p.start()
    # p.join()
