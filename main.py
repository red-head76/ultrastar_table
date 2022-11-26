from ultrastar_table.ultrastar_table import UltrastarTable

if __name__ == "__main__":
    path = "./testset"
    ust = UltrastarTable()
    df = ust.read_from_folder(path)
    print(df)
