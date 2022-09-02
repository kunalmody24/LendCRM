for table in tables.values():
    #     # Determine all the cells that belong to this table
    #     table_cells = [cells[cell_id] for cell_id in get_children_ids(table)]

    #     # Determine the table's number of rows and columns
    #     n_rows = max(cell['RowIndex'] for cell in table_cells)
    #     n_cols = max(cell['ColumnIndex'] for cell in table_cells)
    #     # Create empty 2d array (rows x columns)
    #     content = [[None for _ in range(n_cols)] for _ in range(n_rows)]

    #     # Fill in each cell
    #     for cell in table_cells:
    #         cell_contents = [
    #             words[child_id]['Text']
    #             if child_id in words
    #             else selections[child_id]['SelectionStatus']
    #             for child_id in get_children_ids(cell)
    #         ]
    #         i = cell['RowIndex'] - 1
    #         j = cell['ColumnIndex'] - 1
    #         content[i][j] = ' '.join(cell_contents)

    #     # We assume that the first row corresponds to the column names
    #     dataframe = pd.DataFrame(content[1:], columns=content[0])
    #     dfs.append(dataframe)