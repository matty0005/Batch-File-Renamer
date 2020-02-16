import os
import argparse

parser = argparse.ArgumentParser(description="Rename a bunch of files")
parser.add_argument('--dir','-d', dest='directory', nargs=1, type=str, required=True, metavar="directory", help="The directory containing the files to be renamned")
parser.add_argument('--recursive', '-r', dest='recursive', nargs='?', const=True, help="Allow renaming of sub folders, default=False")

args = parser.parse_args()

rec_paths = []

def validate_dir(directory_to_test):
   return os.path.exists(directory_to_test)

def normalise_dir(directory_to_normalise):
    return os.path.abspath(directory_to_normalise)

def scan(directory):
    """ Scan the directory at one level deep
    
    Parameters:
        directory(str): the normalised path/directory

    Returns:
        list: list containing all the files as an os.DirEntry object.
    """

    files_in_dir = []
    with os.scandir(directory) as d:
        for entry in d:
            if entry.is_file():
                files_in_dir.append(entry)

    return files_in_dir

def scan_rec(directory):
    """ Scan the directory at multiple levels - scan for folders in folders.
    
    Parameters:
        directory(str): the normalised path/directory

    Returns:
        list: list containing all the files as an os.DirEntry object.
    """
    
    with os.scandir(directory) as d:
        for entry in d:
            if entry.is_dir():
                scan_rec(entry.path)
            
            if entry.is_file():
                rec_paths.append(entry)


    return rec_paths

def get_name_partial(path, search_dir):
    """Find the parent and child names for renaming

    Parameters:
        path(str): the absolute path to a file,
        search_dir(str): the search directory passed in

    Returns:
        str: first segment of the name

    """
    path_name = os.path.dirname(path)
        
    if search_dir == path_name:
        elements = path_name.split('\\')
        _name = elements[-1]

    else:
        new_path_name = path_name.replace('{0}\\'.format(search_dir), '')
        _name = '{0} '.format(search_dir.split('\\')[-1]) + new_path_name.replace('\\', ' ')

    return _name


def main():
    #Validate the path, if its legit, continue
    if not validate_dir(args.directory[0]):
        print("Not a valid path")
        return

    #Normalise the path for OS to handle
    directory = normalise_dir(args.directory[0])

    #list all the files and sub directories in the directory
    #If recursive definition is allowed
    if args.recursive:
        rec_paths = []
        files = scan_rec(directory)

    else:
        files = scan(directory)

    print("--- Found {0} files in the directory ---".format(len(files)))

    responded_all = False

    for item in files:
        prefix = get_name_partial(item.path, directory)

        #preseve the file extension
        file_extention = item.name.split('.')[-1]

        #Get the episode number
        pre = item.name.replace('_', ' ')
        l1_split = pre.split()

        #Use the fact that it is a number
        ep_num = None
        for element in l1_split:
            try:
                int(element)
                ep_num = element
            except:
                pass
            if ep_num == None:
                print("Can't determine episode number.")
                
               

        if ep_num != None:

            pre_name = prefix + " - EP " + ep_num + ".{0}".format(file_extention)

            #Prompt the user if this is name is good
            if not responded_all:
                response = "T"
                while response.upper() not in ["Q", "Y", "N", "A"]:
                    print("Is '{0}' a suitable filename? (Y[es], N[o], A[ll], Q[uit])".format(pre_name))
                    response = input("> ")

                if response.upper() == "Q":
                    print("Exiting...")
                    return

                if response.upper() == "N":
                    while response.upper() != "Y":
                        print("Please manually enter a filename with file extension")
                        filename = input("> ")
                        print("Is '{0}' the correct filename? (Y[es], N[o]".format(filename))
                        response = input("> ")

                if response.upper() == "A":
                    responded_all = True

            filename = pre_name

            #Rename the filename
            print(os.path.dirname(item.path) + "\\" + filename)
            os.rename(item.path, os.path.dirname(item.path) + "\\" + filename)



if __name__ == '__main__':
    main()



