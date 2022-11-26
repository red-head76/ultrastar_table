import ultrastar_table
import os
import unittest


class TestUtrastarTable(unittest.TestCase):

    ust = UltrastarTable()

    def test_read_from_folder(folder="./testset"):
        df = ust.read_from_folder(folder)
        self.assertTrue(True)
