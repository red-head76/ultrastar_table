# Copyright

import os
import pathlib
import re
import warnings

import pandas as pd


class UltrastarTable():
    def __init__(self) -> None:
        self._columns = ['Artist', 'Title', 'Directory', 'Cover', 'Video', 'Commentary']
        self._dtypes = {'Artist': str, 'Title': str, 'Directory': str,
                        'Cover': bool, 'Video': bool, 'Commentary': str}
        self.local_df = None

    @staticmethod
    def _set_dtypes(df, dtypes):
        for column in df.columns:
            df[column] = df[column].astype(dtypes[column])

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
                commentary = ''

                dfs.append(pd.DataFrame([dict(zip(self._columns, [artist, title, candidate, cover,
                                                                  video, commentary]))]))
            except:
                warnings.warn(f"{candidate} had wrong format and was skipped.")
        df = pd.concat(dfs, ignore_index=True)
        self._set_dtypes(df, self._dtypes)
        return df


if __name__ == "__main__":
    path = pathlib.Path("./testset")
    ust = UltrastarTable()
    df = ust.read_from_folder(path)
    print(df)
