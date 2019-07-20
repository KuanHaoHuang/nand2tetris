import os, time, pandas

# python3 /Users/WilsonHuang/Downloads/nand2tetris/track_progress.py /Users/WilsonHuang/Downloads/nand2tetris/projects/ 

if (len(os.sys.argv) < 2):
    raise TypeError("no input?")
else:
    if not os.sys.argv[1].endswith("/"):
        os.sys.argv[1] = os.sys.argv[1] + "/"
    if "." in os.sys.argv[1].split("/")[-2]:
        raise TypeError("input possibly a file, not a directory") 
    if not os.path.isdir(os.sys.argv[1]):
        raise TypeError("directory not found")
    print(f"nand2tetris project directory: \n    {os.sys.argv[1]}")

my_dir = os.sys.argv[1]

arr = []
for root, dirs, files in os.walk(my_dir):
    for f in files:
        full_path = os.path.join(root, f)
        ct = time.ctime(os.path.getctime(full_path))
        mt = time.ctime(os.path.getmtime(full_path))
        arr.append(
            {"file_path": full_path,
             "created_time": ct,
             "last_modified_time": mt})

output_dir = os.path.dirname(os.sys.argv[0])
pandas.DataFrame(arr).to_csv(output_dir + "/" + "track_progress.csv", index = False)