import tarfile
from tqdm import tqdm
# Alpha v1
# compress("compressed.tar.gz", ["test.txt", "test_folder"])
# extract("compressed.tar.gz", "extracted")

def extract(tar_file, path=".", members=None):
    tar = tarfile.open(tar_file, mode="r:gz")
    if members is None:
        members = tar.getmembers()
    progress = tqdm(members)
    for member in progress:
        tar.extract(member, path=path)
        progress.set_description("Extracting..")
        progress.unit="b"
        #progress.set_description(f"Extracting.. {member.name}")
    tar.close()


def compress(tar_file, members):
    tar = tarfile.open(tar_file, mode="w:gz")
    progress = tqdm(members)
    for member in progress:
        tar.add(member)
        progress.set_description("Compressing..")
        progress.unit="b"
        #progress.set_description(f"Compressing.. {member}")
    tar.close()
    