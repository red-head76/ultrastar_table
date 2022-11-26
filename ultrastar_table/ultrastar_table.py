# Copyright

import os
import pathlib
import re
import warnings

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
        columns = ['Artist', 'Title', 'Directory', 'Cover', 'Video', 'Commentary']
        dfs = []
        for candidate in candidates:
            try:
                files = os.listdir(path / candidate)
                # Extract Artist and Title information from .txt file
                r = re.compile(r".*\.txt$")
                newlist = list(filter(r.match, files))
                if len(newlist) > 1:
                    raise FileNotFoundError("There are multiple .txt files in the" +
                                            f"subfolder {candidate}")
                txtfile = newlist[0]
                with open(path / candidate / txtfile, "r") as f:
                    data = "".join(f.readlines())
                artist = re.search(r"(?<=#ARTIST:).*?(?=\n)", data).group(0)
                title = re.search(r"(?<=#TITLE:).*?(?=\n)", data).group(0)
                # Check if video is available
                cover = any([re.search(r"(.*\.jpg)|(.*\.png)", file) for file in files])
                video = any([re.search(r"(.*\.mp4)|(.*\.avi)", file) for file in files])
                commentary = None

                dfs.append(pd.DataFrame([dict(zip(columns, [artist, title, candidate, cover,
                                                            video, commentary]))]))
            except:
                warnings.warn(f"{candidate} had wrong format and was skipped.")
        return pd.concat(dfs, ignore_index=True)


if __name__ == "__main__":
    path = pathlib.Path("./testset")
    ust = UltrastarTable()
    df = ust.read_from_folder(path)
    print(df)
