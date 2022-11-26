from ultrastar_table import ultrastar_table
import unittest
import pandas as pd


class TestUtrastarTable(unittest.TestCase):

    def test_read_from_folder(self, folder="./testset"):
        ust = ultrastar_table.UltrastarTable()
        df1 = ust.read_from_folder(folder)
        df2 = pd.DataFrame(columns=['Artist', 'Title', 'Directory', 'Cover', 'Video', 'Commentary'])
        row1 = {'Artist': '257ers',
                'Title': 'Holz',
                'Directory': '257ers - Holz',
                'Cover': True,
                'Video': True,
                'Commentary': ''}
        row2 = {'Artist': 'Culcha Candela',
                'Title': 'Ey DJ',
                'Directory': 'Culcha Candela - Ey DJ',
                'Cover': True,
                'Video': True,
                'Commentary': ''}
        row3 = {'Artist': 'Panic! At The Disco',
                'Title': 'High Hopes',
                'Directory': 'Panic! At The Disco - High Hopes',
                'Cover': True,
                'Video': True,
                'Commentary': ''}
        df2 = pd.concat([df2, pd.DataFrame([row1, row2, row3])])
        # Set proper dtypes
        dtypes = {'Artist': str, 'Title': str, 'Directory': str,
                  'Cover': bool, 'Video': bool, 'Commentary': str}
        for key, val in dtypes.items():
            df2[key] = df2[key].astype(val)
        pd.testing.assert_frame_equal(df1, df2)
