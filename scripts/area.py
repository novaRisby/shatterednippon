from tempfile import mkstemp
from shutil import move
from os import remove, close

num = 778

count = 0
prev_line = ""

fh, abs_path = mkstemp()

with open(abs_path, "w") as new_file:
    with open("area.txt") as old_file:
        for line in old_file:
            x = ""
            if "= {" in prev_line:
                count += 1
                for n in range(count*10-10+1, count*10+1):
                    if n <= num:
                        x = x + "%d " % n
                    else:
                        break
                x += "\n"
                """for line in fileinput.input(directory+file, inplace=True):
                    line = line.rstrip().replace(line, x)
                    print(line)
            """ 
                new_file.write(x)
            else:
                new_file.write(line)
            prev_line = line
            
close(fh)
remove("area.txt")
move(abs_path, "area.txt")
