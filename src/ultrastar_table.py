# Copyright

import os
import pathlib
import pandas as pd

class UtrastarTable():
    def __init__(self) -> None:
        self.local_df = None

    def read_from_folder(self, path):
        """Reads all song names from a given folder
        
        Parameters
        ----------
        path : str, pathlib.Path
            path to the folder
        
        Returns
        -------
        pd.DataFrame
            DataFrame containing all information
        """
        candidates = os.listdir(path)
