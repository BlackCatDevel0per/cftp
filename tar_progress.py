import tarfile
from tqdm import tqdm
# Alpha v1
# compress("compressed.tar.gz", ["test.txt", "test_folder"])
# extract("compressed.tar.gz", "extracted")

def extract(tar_file, path=".", mode="r", members=None):
    if mode=="TAR":
      fext="r"
    elif mode=="TGZ":
      fext="r:gz"
    else:
      print("???")
    
    print(fext)
    tar = tarfile.open(tar_file, mode=fext)
    if members is None:
        members = tar.getmembers()
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        progress.set_description("Extracting..")
        progress.unit="b"
        #progress.set_description(f"Extracting.. {member.name}")
    tar.close()


def compress(tar_file, mode="w", members=None):
    if mode=="TAR":#Check that!!!
      mode="w"
    elif mode=="TGZ":
      mode="w:gz"
    print(mode)

    tar = tarfile.open(tar_file, mode)
    progress = tqdm(members)
    for member in progress:
        tar.add(member)
        progress.set_description("Compressing..")
        progress.unit="b"
        #progress.set_description(f"Compressing.. {member}")
    tar.close()
    