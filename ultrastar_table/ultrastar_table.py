# Copyright

import os
import pathlib
import re

import pandas as pd



class UltrastarTable():
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
        path = pathlib.Path(path)
        candidates = os.listdir(path)
        df = pd.DataFrame(columns=['Artist', 'Title', 'Directory', 'Cover', 'Video', 'Commentary'])
        for candidate in candidates:
            files = os.listdir(path / candidate)
            r = re.compile("\.txt$")
            newlist = list(filter(r.match, files))
            if len(newlist) > 1:
                raise FileNotFoundError(f"There are multiple .txt files in the subfolder {candidate}")
            with open(path / candidate, "r") as f:
                data = f.readlines()
                breakpoint()


if __name__ == "__main__":
    path = pathlib.Path("./testset")
    ust = UltrastarTable()
    ust.read_from_folder(path)

    
