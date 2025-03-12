from jnius import autoclass


def serialize_map_to_dict(hash_map):
    map_to_dict_data = {}

    for key, value in zip(hash_map, hash_map.values()):
        if hasattr(value, "put"):
            map_to_dict_data[key] = serialize_map_to_dict(value)
        elif hasattr(value, "add"):
            map_to_dict_data[key] = serialize_array_to_list(value)
        else:
            map_to_dict_data[key] = value
    return map_to_dict_data


def serialize_array_to_list(array):
    array_to_list_data = []

    for value in array:
        if hasattr(value, "add"):
            data = serialize_array_to_list(value)
            array_to_list_data.append(data)
        elif hasattr(value, "put"):
            data = serialize_map_to_dict(value)
            array_to_list_data.append(data)
        else:
            array_to_list_data.append(value)
    return array_to_list_data


def serialize_dict_to_map(dictionary):
    dict_to_map_data = autoclass("java.util.HashMap")()

    for key, value in dictionary.items():
        if isinstance(value, dict):
            data = serialize_dict_to_map(value)
            dict_to_map_data.put(key, data)
        elif isinstance(value, list):
            data = serialize_list_to_array(value)
            dict_to_map_data.put(key, data)
        else:
            dict_to_map_data.put(key, value)
    return dict_to_map_data


def serialize_list_to_array(list_):
    list_to_array_data = autoclass("java.util.ArrayList")()

    for value in list_:
        if isinstance(value, list):
            data = serialize_list_to_array(value)
            list_to_array_data.add(data)
        elif isinstance(value, dict):
            data = serialize_dict_to_map(value)
            list_to_array_data.add(data)
        else:
            list_to_array_data.add(value)
    return list_to_array_data


if __name__ == "__main__":
    # Serialize Java map to Python dictionary
    hm = autoclass("java.util.HashMap")()
    hm.put("ada", "kene")
    hm.put("kene", "ada")

    bm = autoclass("java.util.HashMap")()
    bm.put("ken", 1)
    bm.put(2, 3)

    cm = autoclass("java.util.HashMap")()

    ar = autoclass("java.util.ArrayList")()
    ar.add(1)
    ar.add(2)
    ar.add(bm)
    # cm.put("hj", ar)
    #
    # bm.put("extras", cm)
    hm.put("extra", ar)
    print(serialize_map_to_dict(hm))

    # Serialize Java array to Python list
    al = autoclass("java.util.ArrayList")()
    al.add(1)
    al.add("ada")

    dm = autoclass("java.util.HashMap")()
    dm.put("ada", "kene")

    al.add(dm)
    print(serialize_array_to_list(al))

    # Serialize Python dictionary to Java map
    dt = {"ada": "kene", 1: [{"1": "ada"}]}
    print(serialize_dict_to_map(dt).get(1).get(0).get("1"))

    # Serialize Python list to Java Array
    lt = [1, 2, 3, {"ada": "kene"}]
    print(serialize_list_to_array(lt))
