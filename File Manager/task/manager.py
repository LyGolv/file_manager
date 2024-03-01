import math
import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


class CMD:
    @staticmethod
    def pwd(_):
        print(os.getcwd())

    @staticmethod
    def cd(arg):
        if arg[0] == "..":
            os.chdir('/'.join(os.getcwd().split("/")[:-1]))
            print(os.getcwd())
        elif arg:
            try:
                os.chdir(os.getcwd() + "/" + arg[0])
            except FileNotFoundError:
                print("No such file or directory")
            print(arg[0])

    @staticmethod
    def ls(arg):
        if not arg:
            dirs, files = [], []
            for file in os.listdir():
                if os.path.isdir(file):
                    dirs.append(file)
                else:
                    files.append(file)
            print("\n".join(dirs))
            print("\n".join(files))
        elif arg[0] == "-l":
            for file in os.listdir():
                print(file, os.stat(file).st_size)
        elif arg[0] == "-lh":
            for file in os.listdir():
                size_suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
                size = os.stat(file).st_size
                index = math.floor(math.log(size, 1024))
                index = index if index < len(size_suffixes) else len(size_suffixes) - 1
                size = size if index == 0 else round(size / 1024 * index)
                print(file, f"{size}{size_suffixes[index]}")

    @staticmethod
    def rm(arg):
        if not arg:
            print("Specify the file or directory")
        else:
            for file in arg:
                try:
                    if file.startswith("."):
                        find = False
                        for f in os.listdir():
                            if os.path.isfile(f) and f.endswith(file):
                                os.remove(file)
                                find = True
                        if not find:
                            print(f"File extension {file} not found in this directory")
                    elif os.path.isdir(file):
                        shutil.rmtree(file)
                    else:
                        os.remove(file)
                except FileNotFoundError:
                    print(f"No such file or directory")

    @staticmethod
    def mv(arg):
        if len(arg) != 2:
            print("Specify the current name of the file or directory and the new location and/or name")
        else:
            if os.path.isfile(arg[1]):
                print("The file or directory already exists")
            elif arg[0].startswith("."):
                find = False
                for f in os.listdir():
                    if os.path.isfile(f) and f.endswith(arg[0]):
                        find = True
                        if os.path.isfile(arg[1]+"/"+f):
                            choice = "*"
                            while choice not in "yYnN":
                                choice = input(f"{f} already exists in this directory. Replace? (y/n)\n")
                            if choice in "nN":
                                continue
                            else:
                                os.remove(arg[1]+"/"+f)
                        shutil.move(f, arg[1])
                if not find:
                    print(f"File extension {arg[0]} not found in this directory")
            else:
                try:
                    shutil.move(arg[0], arg[1])
                except FileNotFoundError:
                    print(f"No such file or directory")

    @staticmethod
    def mkdir(arg):
        if not arg:
            print("Specify the name of the directory to be made")
        else:
            try:
                os.mkdir(arg[0])
            except FileExistsError:
                print("The directory already exists")

    @staticmethod
    def cp(arg):
        if not arg:
            print("Specify the file")
        elif len(arg) == 2:
            if arg[0].startswith("."):
                find = False
                for f in os.listdir():
                    if os.path.isfile(f) and f.strip().endswith(arg[0]):
                        find = True
                        if os.path.isfile(arg[1]+"/"+f):
                            choice = "*"
                            while choice not in "yYnN":
                                choice = input(f"{f} already exists in this directory. Replace? (y/n)\n")
                            if choice in "nN":
                                continue
                        shutil.copy(f, arg[1])
                if not find:
                    print(f"File extension {arg[0]} not found in this directory")
            else:
                try:
                    shutil.copy(arg[0], arg[1])
                except FileNotFoundError:
                    print(f"No such file or directory")
                except shutil.SameFileError:
                    print(f"{arg[0]} already exists in this directory")
        else:
            print("Specify the current name of the file or directory and the new location and/or name")


def main():
    # put your code here
    print("Input the command")
    while True:
        command, *arg = input().split()
        if command == "quit":
            break

        if hasattr(CMD, command):
            getattr(CMD, command)(arg)
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
