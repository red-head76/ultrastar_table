from ultrastar_table.ultrastar_table import UltrastarTable

if __name__ == "__main__":
    ust = UltrastarTable()
    ust.update_dfs()
    ust.merge_dfs()
    ust.write_to_spreadsheet()
