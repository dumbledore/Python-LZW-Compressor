import os, time, sys
from constants import *

def get_input_code(f, large_dict):
    # returns a number

    if large_dict:
        b = f.read(3)
        if len(b) != 3: return None # raise exception?
        return (b[0] << 16) + (b[1] << 8) + b[2]
    else:
        b = f.read(2)
        if len(b) != 2: return None # raise exception?
        return (b[0] << 8) + b[1]

def output_pattern_for_code(o, pattern):
    o.write(pattern) #pattern is just bytes

def decompress_more(f, o, large_dict):

    string_table = {x : bytes([x]) for x in range(256)}
    dict_size = 257

    more_to_decompress = False

    prev_code = get_input_code(f, large_dict)
    if prev_code is None: return False #Nothing to decompress
    k = bytes([prev_code])
    output_pattern_for_code(o, k)

    while True:
        curr_code = get_input_code(f, large_dict)
        if curr_code is None: break #EOF reached
        if curr_code == DICT_FLUSHED:
            return True
        
        if curr_code not in string_table:
            pattern = string_table[prev_code]
            pattern += k
        else:
            pattern = string_table[curr_code]
        output_pattern_for_code(o, pattern)
        k = pattern[0:1]
        string_table[dict_size] = string_table[prev_code] + k
        dict_size += 1
        
        prev_code = curr_code

    return more_to_decompress

def decompress(file_in, file_out):
    f = None
    o = None

    t = time.time()

    try:
        # open files
        f = open(file_in, 'rb')

        #read header
        if f.read(len(LZW_HEADER)) != LZW_HEADER:
            raise ArchiveError("File is not in LZW format.")

        large_dict = f.read(1)
        if large_dict == b'\x00': large_dict = False
        else: large_dict = True

        # All OK, open file for writing then.
        o = open(file_out, 'wb')

        # decompressing file
        print("Decompressing...")
        while decompress_more(f, o, large_dict): pass

    finally:
        if f is not None: f.close()
        del f
        
        if o is not None: o.close()
        del o

    flen = os.path.getsize(file_in)
    olen = os.path.getsize(file_out)
    print("Compression ratio is ", round((olen/flen)*100), "%")
    print("Job completed in ", round(time.time() - t), " seconds")

def process_command_line(arguments, automated = False):
#    .lower().endswith("lzw")
    usage ="""
--- Usage ---
decompress.py <infile> [<outfile>]

If <infile> ends in .lzw, then <outfile> defaults to <infile> with .lzw removed.
Otherwise <outfile> defaults to <infile>.decompressed
"""

    if len(arguments) < 2:
        if not automated: print(usage)
        return

    if arguments[1] == 'help' or arguments[1] == '/h' or arguments[1] == '-h':
        if not automated: print(usage)
        return

    if not os.path.exists(arguments[1]) or not os.path.isfile(arguments[1]):
        if not automated:
            print()
            print("The file <", arguments[1], "> does not exist")
            print(usage)
        return

    file_in = arguments[1]

    if len(arguments) > 2:
        file_out = arguments[2]
    else:
        if file_in.lower().endswith('.lzw'):
            file_out = file_in[:-4]
        else:
            file_out = file_in + '.decompressed'

    if os.path.exists(file_out) and os.path.isfile(file_out):
        if not automated:
            answer = ''
            print("A filename with the same name as the output file exists. Would you like to overwrite it?")
            while answer == '':
                answer = input('(Y/N):')

            if answer != 'y' and answer != 'Y': return #The user hit the road
        else:
            return #emulate cancellation

    print('Decompressing <', file_in, '> into <', file_out, '>')
    try:
        decompress(file_in, file_out)
    except ArchiveError:
        if not automated: print("Unsupported file type or the archive is corrupted")
        return

if __name__ == '__main__':
    processed = process_command_line(sys.argv)
    if processed is not None:
        # input was valid
        decompress(*processed)
