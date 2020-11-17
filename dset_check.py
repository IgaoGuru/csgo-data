from datasetcsgo import CsgoDataset
from datasetcsgo import dataset_check
import argparse

parser = argparse.ArgumentParser(description="check csgo-data style dataset")
parser.add_argument("-rp", help='the absolute path the root directory of the csgo-data-style dataset to be checked', type=str)
args = parser.parse_args()
root_path = args.rp

print("checking dataset, please wait a minute while we load the images!")
dataset = CsgoDataset(root_path)
print("what session do you want to check?:")

for idx, sesh in enumerate(dataset.session_lens.keys()):
    print(f"#{idx}: {sesh} [{dataset.session_lens[sesh][0]-dataset.session_lens[sesh][1]} images]")
print("\n choose the sessions (space separated):")
inpt = input()

if inpt == "all":
    seshs = range(len(dataset.session_lens.keys()))
elif " " not in inpt:
    seshs = [int(inpt)]
else:
    seshs = list(map(int, input().split()))
    
dataset_check(dataset, seshs)