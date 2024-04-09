import math

recipies = {
    "en smlt": {"redstone": 4, "glass": 2, "bcc": 2, "steel case": 1},
    "chem diss cmbr": {"en obs ingot": 4, "ctank": 2, "ucc": 2, "steel case": 1},
    "chem wash": {"en obs ingot": 4, "ctank": 1, "ftank": 1, "ucc": 2, "steel case": 1},
    "chem cryst": {"ucc": 2, "steel case": 1, "fluorite": 2, "en obs ingot": 4},
    "chem inj cmbr": {"elite alloy": 4, "ecc": 2, "gold": 2, "pure cmbr": 1},
    "pure cmbr": {"en alloy": 4, "acc": 2, "osmium": 2, "en cmbr": 1},
    "crusher": {"redstone": 4, "bcc": 2, "steel case": 1, "lava bucket": 2},
    "en cmbr": {"redstone": 4, "bcc": 2, "iron": 2, "steel case": 1},
    "thrm evap plnt": {"thrm evap blk": 33, "adv solar": 4, "thrm evap ctrl": 1, "thrm evap valv": 2},
    "elec sep": {"iron": 4, "redstone": 2, "en alloy": 2, "elec core": 1},
    "chem inf": {"bcc": 2, "en alloy": 2, "ctank": 2, "steel case": 1},
    "rot cond": {"energy tablet": 1, "bcc": 2, "glass": 4, "ctank": 1, "ftank": 1},
    "chem ox": {"personal chest": 1, "ctank": 1, "en alloy": 4, "bcc": 2, "dynamic tank": 1},
    "iso cent": {"lead": 6, "ucc": 2, "ctank": 1},
    "bcc": {"osmium": 1},
    "ctank": {"redstone": 4, "osmium": 4},
    "ftank": {"redstone": 4, "iron": 4},
    "steel case": {"steel": 4, "osmium": 1, "glass": 4},
    "acc": {"bcc": 1, "en alloy": 2},
    "ecc": {"acc": 1, "elite alloy": 2},
    "ucc": {"ecc": 1, "ult alloy": 2},
    "personal chest": {"steel": 5, "glass": 1, "bcc": 1, "chest": 2},
    "en alloy": {"iron": 1},
    "elite alloy": {"en alloy": 1, "diamond": 0.25},
    "ult alloy": {"elite alloy": 1, "en obs dust": 0.5},
    "en obs dust": {"obs dust": 1, "diamond": 1/8},
    "en obs ingot": {"en obs dust": 1},
    "thrm evap blk": {"steel": 1, "copper": 1/4},
    "thrm evap valv": {"thrm evap blk": 4, "acc": 1},
    "thrm evap ctrl": {"acc": 2, "glass pane": 1, "bucket": 1, "thrm evap blk": 4},
    "adv solar": {"basic solar": 4, "en alloy": 2, "iron": 3},
    "basic solar": {"pv panel": 3, "iron": 1, "osmium": 2, "energy tablet": 1, "en alloy": 2},
    "pv panel": {"glass pane": 3, "redstone": 2, 'en alloy': 1, 'osmium': 3},
    "obs dust": {"obsidian": 1/4},
    "bcc": {"osmium": 1},
    "elec core": {'en alloy': 5, 'gold dust': 1, 'osmium dust': 2, 'iron dust': 1},
    "sna": {'elite alloy': 2, 'ecc': 2, 'steel case': 1, 'bronze': 3, 'hdpe sheet': 1},
    'prc': {'en cmbr': 1, 'bcc': 2, 'ctank': 2, 'steel': 2, 'en alloy': 1, 'dynamic tank': 1},
    'hdpe sheet': {'hdpe pellet': 8},
    'energy tablet': {'gold': 3, 'en alloy': 2, 'redstone': 4},
    'dynamic tank': {'steel': 1, 'bucket': 1/4},
    'lava bucket': {'lava': 1, 'bucket': 1},
    'bucket': {'iron': 3},
    'ind cell': {'lithium dust': 4, 'energy tablet': 4, 'bec': 1},
    'bec': {'iron': 2, 'redstone': 4, 'steel case': 1, 'energy tablet': 2}
}

# roots = {
#     'thrm evap plnt': 1
# }

roots = {
    'ind cell': 10,
}

mats = set(recipies.keys()).union(mat for recipie in recipies.values() for mat in recipie.keys())

parents = {mat: [] for mat in mats}
for target, use in recipies.items():
    for mat in use:
        parents[mat].append(target)

counts = {mat: roots[mat] if mat in roots else 0 for mat in mats}

done = set()
while not all(len(parent) == 0 for parent in parents.values()):
    for mat, parent in parents.items():
        if len(parent) == 0 and mat not in done:
            done.add(mat)
            count = counts[mat]
            if mat in recipies:
                for needed, quant in recipies[mat].items():
                    counts[needed] += quant * count
                    parents[needed].remove(mat)
    
print('Base Mats:', [mat for mat in mats if counts[mat] > 0 and mat not in recipies])

print(counts)

with open('graph.txt', 'w') as file:
    print('digraph {', file=file)
    for mat, count in counts.items():
        if count == 0:
            continue
        print(f'    "{mat}" [shape=hexagon, xlabel={count}]', file=file)

    for recipie, needed in recipies.items():
        if counts[recipie] == 0:
            continue
        for need in needed:
            print(f'    "{need}" -> "{recipie}"', file=file)
    print('}', file=file)

