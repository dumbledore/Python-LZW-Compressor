import os

def compare_more(f1, f2):
    buffer_1 = f1.read(1024*1024)
    buffer_2 = f2.read(1024*1024)

    if len(buffer_1) != len(buffer_2):
        return None, False

    if len(buffer_1) == 0:
        return False, True

    for i in range(len(buffer_1)):
        if buffer_1[i] != buffer_2[i]:
            return None, False
    
    return True, True

def compare_files(file_1, file_2):
    if os.path.getsize(file_1) != os.path.getsize(file_2):
        return False

    f1 = None
    f2 = None

    try:
        f1 = open(file_1, 'rb')
        f2 = open(file_2, 'rb')

        while True:
            more_to_compare, the_same_up_to_now = compare_more(f1, f2)
            if not the_same_up_to_now: return False
            if not more_to_compare: return the_same_up_to_now

    finally:
        if f1 is not None:
            f1.close()
            del f1

        if f2 is not None:
            f2.close()
            del f2
