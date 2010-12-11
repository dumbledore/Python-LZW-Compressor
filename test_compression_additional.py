import unittest, os
from compress import compress
from decompress import decompress
from compare_files import compare_files

FILE_COMPRESSED_NAME = "compr"
FILE_DECOMPRESSED_NAME = "decompr"

class MB700XMLCompressionTest(unittest.TestCase):


    def test_bmp_file_1(self):
        file_orig = "./testdata/additional/bmp/dumbledore.bmp"
        compress(file_orig, FILE_COMPRESSED_NAME, 1024 * 1024, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_bmp_file_2(self):
        file_orig = "./testdata/additional/bmp/poirot_new.bmp"
        compress(file_orig, FILE_COMPRESSED_NAME, 1024 * 1024, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)

    def test_pdf_file(self):
        file_orig = "./testdata/additional/pdf/Izb_04_08.pdf"
        compress(file_orig, FILE_COMPRESSED_NAME, 1024 * 1024, False)
        decompress(FILE_COMPRESSED_NAME, FILE_DECOMPRESSED_NAME)
        self.assertTrue(compare_files(file_orig, FILE_DECOMPRESSED_NAME))
        os.remove(FILE_COMPRESSED_NAME)
        os.remove(FILE_DECOMPRESSED_NAME)
        
if __name__ == "__main__":
    unittest.main()
