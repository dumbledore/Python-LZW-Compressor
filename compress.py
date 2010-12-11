import os, time, sys
from constants import *

bytes_dict = {x : bytes([x]) for x in range(256)} # fast transform from int to byte

def output_code_for_pattern(buffer_writer, position, code, large_dict):
    if large_dict:
        buffer_writer[position] = code >> 16
        buffer_writer[position+1] = (code >> 8) & 0xFF
        buffer_writer[position+2] = code & 0xFF
    else:
        buffer_writer[position] = (code >> 8) & 0xFF
        buffer_writer[position+1] = code & 0xFF

def output_code_for_pattern_to_disc(buffer_writer, position, o):
    if position < len(buffer_writer):
        o.write(buffer_writer[0:position])

def compress_more(f, o, buffer_size, dict_size_large, flen, read_overall, t):

    string_table = {bytes([x]) : x for x in range(256)}
    dict_size = 257 # including DICT_FLUSHED

    if dict_size_large:
        dict_max_size = DICT_SIZE_LARGE
        bytes_per_code = 3
    else:
        dict_max_size = DICT_SIZE_SMALL
        bytes_per_code = 2

    pattern = f.read(1)
    if pattern == f: return False # nothing to be read now so nothing more to be read either

    buffer_reader = f.read(buffer_size)
    if len(buffer_reader) == 0: return False, read_overall #nothing to read

    buffer_writer = bytearray(bytes_per_code * buffer_size) #as more than one byte is used

    read_so_far = 0
    written_so_far = 0
    
    for i in buffer_reader:
        k = bytes_dict[i]
        read_so_far += 1
        
        pattern_k = pattern + k
        if pattern_k not in string_table:
            if dict_size == dict_max_size:
                # dict is full
                output_code_for_pattern(buffer_writer, written_so_far, string_table[pattern], dict_size_large)
                written_so_far += bytes_per_code
                output_code_for_pattern(buffer_writer, written_so_far, DICT_FLUSHED, dict_size_large)
                written_so_far += bytes_per_code
                f.seek(-1 - len(buffer_reader) + read_so_far, 1)
                output_code_for_pattern_to_disc(buffer_writer, written_so_far, o)

                read_overall += read_so_far
                return True, read_overall # dict's been filled-up to the rim; there's probably more to compress
            
            output_code_for_pattern(buffer_writer, written_so_far, string_table[pattern], dict_size_large)
            written_so_far += bytes_per_code
            string_table[pattern_k] = dict_size
            dict_size += 1
            pattern = k
        else:
            pattern = pattern_k

    output_code_for_pattern(buffer_writer, written_so_far, string_table[pattern], dict_size_large)
    written_so_far += bytes_per_code
    output_code_for_pattern(buffer_writer, written_so_far, DICT_FLUSHED, dict_size_large)
    written_so_far += bytes_per_code
    output_code_for_pattern_to_disc(buffer_writer, written_so_far, o) # print compressed data to output in one step

    read_overall += read_so_far
    return True, read_overall # probably there is still something more to fill the buffer with?

def compress(file_in, file_out, buffer_size, large_dict):
    f = None
    o = None
 
    t = time.time()

    global bytes_written
    bytes_written = 0

    try:
        # open files
        f = open(file_in, 'rb')
        o = open(file_out, 'wb')

        # writing header
        o.write(LZW_HEADER)
        o.write(bytes([large_dict]))

        # compressing file
        print("Compression started...")
        
        flen = os.path.getsize(file_in)
        if flen == 0: return
        
        read_overall = 0

        more_to_compress = True
        while more_to_compress:
            more_to_compress, read_overall = compress_more(f, o, buffer_size, large_dict, flen, read_overall, t)
            eta = round((round(time.time() - t) / read_overall) * (flen-read_overall))
            percent = round((read_overall / flen) * 100, 2)
            print(percent, "%, ETA:", eta, "sec")

    finally:
        if f is not None: f.close()
        del f
        
        if o is not None: o.close()
        del o

    olen = os.path.getsize(file_out)
    print("Compression ratio is ", round((olen/flen)*100), "%")
    print("Job completed in ", round(time.time() - t), " seconds")

def process_command_line(arguments, automated = False):
    usage ="""
--- Usage ---
compress.py <infile> [<outfile>] [-012]

<outfile> defaults to <infile>.lzw

numbers define compression method:
    0: general compression                ; uses  1MB buffer and 64K dictionary; uses around   6MB RAM, ~35%
    1: special compression for large files; uses 16MB buffer and 16M dictionary; uses around 200MB RAM, ~31%
    2: special compression for large files; uses 32MB buffer and 16M dictionary; uses around 400MB RAM, ~29%
"""
    help ="""
if you need help, just call it like that: compress.py help
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
            print(help)
        return

    file_in = arguments[1]

    if os.path.getsize(file_in) < SMALLEST_PERMITTED_SIZE:
        if not automated:
            print()
            print("The file is too small to be effectively compressed")
        return
    
    compressions = {'-0': COMPRESSION_1MB_64KB, '-1' : COMPRESSION_16MB_16MB, '-2': COMPRESSION_32MB_16MB}
    compression  = COMPRESSION_1MB_64KB

    # then the output filename must be guessed (just in case)
    file_out = file_in + '.lzw'

    if len(arguments) > 2:
        if arguments[2] in compressions:
            compression = compressions[arguments[2]]
        else: #then the filename is given
            file_out = arguments[2]

        # Test if the output path is valid not made (How?)
        if file_in == file_out:
            if not automated: 
                print()
                print("The output file is the same as the input file")
            return
        
    if os.path.exists(file_out) and os.path.isfile(file_out):
        if not automated: 
            answer = ''
            print("A filename with the same name as the output file exists. Would you like to overwrite it?")
            while answer == '':
                answer = input('(Y/N):')

            if answer != 'y' and answer != 'Y': return #The user hit the road
        else:
            return # emulate cancellation

    if len(arguments) > 3:
        #compression method
        if arguments[3] in compressions:
            compression = compressions[arguments[3]]
        else:
            if not automated: 
                print()
                print("Invalid compression specifiec as the third argument")
                print(help)
            return

    buffer, long_dict = COMPRESSIONS[compression]
    if not automated: print('Compressing <', file_in, '> into <', file_out, '> using', buffer/1024/1024, 'MB buffer and Using ', DICT_SIZE[long_dict]/1024, 'KB DICT')
    compress(file_in, file_out, buffer, long_dict)
    
if __name__ == '__main__':
    processed = process_command_line(sys.argv)
    if processed is not None:
        # input was valid
        compress(*processed)
