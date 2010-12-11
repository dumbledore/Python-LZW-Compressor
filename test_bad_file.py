import unittest, os
from decompress import decompress
from constants import ArchiveError

FILE_COMPRESSED_NAME = "compr"
FILE_DECOMPRESSED_NAME = "decompr"

class ArchiveErrorTest(unittest.TestCase):

    def test_not_lzw_file(self):
        file_orig = "./data/basic/MB0064"
        self.assertRaises(ArchiveError)
       
if __name__ == "__main__":
    unittest.main()
