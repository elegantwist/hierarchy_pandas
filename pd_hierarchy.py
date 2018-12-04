import pandas as pd
from tqdm import tqdm

MaxDepth = 4
QuantCategory = 100
QuantIdLenth = len(str(QuantCategory)) - 1


def fill_an_example_table():

    MaxItems = 50

    ItemName = "TheItem_"

    df = pd.DataFrame()

    for i in range(MaxItems):

        print(i)

        res2 = None
        res2 = []
        for i2 in tqdm(range(MaxItems)):

            res = None
            res = []

            for i_i in range(MaxItems):

                for m in range(MaxItems):

                    str_id = ("0" + str(i))[-QuantIdLenth:] + \
                             ("0" + str(i2))[-QuantIdLenth:] + \
                             ("0" + str(i_i))[-QuantIdLenth:] + \
                             ("0" + str(m))[-QuantIdLenth:]

                    id = int(str_id)

                    res = res + [{
                        "Id": id,
                        "Str_Id": str_id,
                        "Name": ItemName + str_id
                    }]

            res2 = res2 + res

        df = df.append(res2).reset_index(drop=True)

    return df


def get_min_max_coordinates(depth=0, coordinates_from=0):

    gr_quant = QuantCategory ** (depth - 1)

    coordinates_to = coordinates_from + gr_quant - 1

    return coordinates_from, coordinates_to, gr_quant/QuantCategory


def get_depth(group_id=0):

    str_group_id = str(group_id)

    depth = 1
    while 1:
        right_digits = str_group_id[-QuantIdLenth:]

        if right_digits != '00':
            break

        depth = depth + 1

        str_group_id = str_group_id[:-QuantIdLenth]

        if len(str_group_id) < QuantIdLenth:
            break

    return depth


def get_subgroup_list(df=None, groups=[]):

    res_subgroups = pd.DataFrame()

    for i_gr in groups:

        depth = get_depth(i_gr)

        subgroup_coordinates_min, subgroup_coordinates_max, group_quant = get_min_max_coordinates(depth=depth, coordinates_from=i_gr)

        all_subgroups = df[df.eval("(index >= "+str(subgroup_coordinates_min)+") & (index <= "+str(subgroup_coordinates_max)+") & ((index % "+str(group_quant)+") == 0)")]

        res_subgroups = res_subgroups.append(all_subgroups, ignore_index=True)

    return res_subgroups


def get_items_list(df=None, groups=[]):

    res_items = pd.DataFrame()

    for i_gr in groups:

        depth = 2

        items_coordinates_min, items_coordinates_max, _ = get_min_max_coordinates(depth=depth, coordinates_from=i_gr)

        all_items = df[df.eval("(index >= "+str(items_coordinates_min)+") & (index <= "+str(items_coordinates_max)+")")]

        res_items = res_items.append(all_items, ignore_index=True)

    return res_items


df = fill_an_example_table()

import datetime

df = df.set_index('Id')

n_date = datetime.datetime.now()

all_subgroups = get_subgroup_list(df, groups=[1000000, 20500, 20000])

print("len of all subgroups: " + str(len(all_subgroups)))

all_items = get_items_list(df, groups=[20500, 1000000])

print("len of all items: " + str(len(all_items)))

print(str(datetime.datetime.now()-n_date))

exit()





