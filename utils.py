import os

def get_files_by_suffix(folder, suffix):
    files = [item for item in os.listdir(folder) if item[-len(suffix):]==suffix]
    return files

def create_path(path):
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except:
            print("create path error")


#########################################################
# test
#########################################################


# for item in get_all_samples():
#     print(item)
