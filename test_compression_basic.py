import unittest, os
from compress import compress
from decompress import decompress
from compare_files import compare_files

FILE_COMPRESSED_NAME = "compr"
FILE_DECOMPRESSED_NAME = "decompr"

class BasicXMLCompressionTest(unittest.TestCase):


    def test_0b_file(self):
        file_orig = "./testdata/basic/BB0000"
        compress(file_orig, FILE_COMPRESSED_NAME, 1000, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_4b_file(self):
        file_orig = "./testdata/basic/BB0004"
        compress(file_orig, FILE_COMPRESSED_NAME, 1000, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_4kb_file(self):
        file_orig = "./testdata/basic/KB0004"
        compress(file_orig, FILE_COMPRESSED_NAME, 1000, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_122kb_file(self):
        file_orig = "./testdata/basic/KB0122"
        compress(file_orig, FILE_COMPRESSED_NAME, 3500, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_122kb_file_16mb_dict(self):
        file_orig = "./testdata/basic/KB0122"
        compress(file_orig, FILE_COMPRESSED_NAME, 3500, True)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)
        
if __name__ == "__main__":
    unittest.main()
