def count_of_type(type):
    if type == 1 or type == 3 or type == 5:
        return 1
    if type == 2 or type == 4 or type == 6:
        return 2
    if type == 9:
        return 3
    if type == 0 or type == 7:
        return 4
    return type // 100 + 1


def offset_to_address(offset):
    return offset + (0x400000 if offset < 0xC4000 else 0x750000)
