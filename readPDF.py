#from operator import concat
#import pdf2image
#import boto3
import re
from PIL import Image
import io
#import pandas as pd
import tabula

# ltc dictionary: keys are ranges of ltc values, and values are indexes
ltc = {}
# ltv dictionary: keys are levels and values are max loan allowed/ LTV values
# (as a list)
ltv_max = {}
# levels dictionary: keys are range of houses flipped and values are indexes
levels = {}
# rates array
rates = []
# Credit score adjustments dictionary: keys are credit score, values are
# a list of 
credit_dict = {}
# states dictionary
states = {"Alabama": "AL", "Alaska": "AK","Arizona": "AZ","Arkansas": "AR", 
          "California": "CA", "Colorado": "CO", "Connecticut": "CT", 
          "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", 
          "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", 
          "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", 
          "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", 
          "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", 
          "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", 
          "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", 
          "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", 
          "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", 
          "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", 
          "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", 
          "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", 
          "Wisconsin": "WI", "Wyoming": "WY"}
# State rate adjustment dictionary: keys are state abbreviations and values
# are adjustments to the interest rate
state_adj = {}
# Ineligible States list: all states listed are ineligible to be considered for
# a loan
ineligible = []

def main():
    # Path of pdf
    path = "Loans3.pdf"
    dfs = tabula.read_pdf(path, multiple_tables=True)
    # NOTE: if multiple tables are in the same row, tabula puts them into
    # one dataframe. We must first identify mutltiple tables within a dataframe
    # and then separate them.
    # for df in dfs:
    #     print(df)
    #     print(list(df.columns.values))
    # Convert all pdf pages to images
    # images = pdf2image.convert_from_path(path)
    # # Save the very first page of the pdf document (that's all we care about)
    # images[0].save("loans.jpg")
    # # Load the image we just saved
    # img = Image.open('loans.jpg')
    # buffered = io.BytesIO()
    # img.save(buffered, format='PNG')
    # client = boto3.client('textract')
    # response = client.analyze_document(
    #     Document={'Bytes': buffered.getvalue()},
    #     FeatureTypes=['TABLES', 'FORMS']
    # )
    # # Convert the response we got from textract to pandas dataframes
    # blocks = response['Blocks']
    # tables = map_blocks(blocks, 'TABLE')
    # cells = map_blocks(blocks, 'CELL')
    # words = map_blocks(blocks, 'WORD')
    # selections = map_blocks(blocks, 'SELECTION_ELEMENT')
    # dfs = []
    # for table in tables.values():
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
    # Plan for Loan Factors Table:
    # 2 dictionaries: a levels dictionary, with keys being range of houses
    # flipped and the value being an index (this index will be used later on),
    # and a ltc dictionary with the keys being the range of ltc values, and the
    # value being another index. Finally, there will be a rates 2d array, which
    # will hold all the rates. Each row in the array will hold all the
    # rates for a certain level (platinum, level1, level2, etc) and each column
    # will hold all the rates for a particular range of ltc values. This way,
    # the two indices from the dictionaries will help determine the corresponding 
    # rate for a level and ltc value
    
    # A list which contains all the possible rowHeaders that could appear in
    # the Loan Factors table
    loanFactors = ['fix/flip', 'ltc', 'ltv', 'max simultaneous']
    tableType = 0
    # Biggest loop, iterates over each table
    for df in dfs:
        print(df)
        # First step is to figure out what type of table it is
        # Extract column headers: this will help us figure out what type of
        # table it is
        headers = list(df.columns.values)
        print("HEADERS" + str(headers))
        # tableType = tableType(headers)
        match tableType:
            # This is the Loan Factors Table (tableType = 0)
            case 0:
                # Initialize the rates array based on the number of columns
                createRates(len(headers) - 1)
                # Package all rows into lists (a list of lists)
                listRows = df.values.tolist()
                # Feed each list to the correct method depending on index0
                for row in listRows:
                    # Extract rowHeader and convert to lowercase
                    row[0] = row[0].lower()
                    rowHeader = row[0]
                    # What type of row is it? Based off rowHeader
                    if loanFactors[0] in rowHeader:
                        # This means we are creating the levels
                        createLevels(row)
                    elif loanFactors[1] in rowHeader:
                        # This means are on an ltc row
                        ltcRow(row)
                        ratesColumn(row)
                    elif loanFactors[2] in rowHeader:
                        # This means we are on an ltv row
                        maxOrLTV(row, 1)
                    elif loanFactors[3] in rowHeader:
                        # This means we are on the max simultaneous row
                        maxOrLTV(row, 0)
                    else:
                        print("ROW NOT RECOGNIZED IN LOAN FACTORS TABLE \n")
            # This is the state rate adjustments table
            case 3:
                # Package all rows into lists (a list of lists)
                listRows = df.values.tolist()
                # For each row in the table, call the function
                for row in listRows:
                    statesRates(row)
        tableType += 1
    # print(state_adj)
    # All dictionaries have been defined. Let's see if it works
    # housesFlipped = (int) (input("ENTER THE NUMBER OF HOUSES FLIPPED IN THE LAST TWO YEARS: "))
    # ltcVal = (float) (input("ENTER AN LTC VALUE: "))
    # findRate(housesFlipped, ltcVal)

# This function will find the correct function to call depending on the type
# of table
# def tableType(headers):
    


def printTables(dfs):
    for df in dfs:
        print(df)

# Create empty 2d array with the correct number of rows (number of levels in
# the matrix)
def createRates(numRows):
    for _ in range(0, numRows):
        row = []
        rates.append(row)

def maxOrLTV(row, index):
    # We skip the first cell because it has no relevant information
    i = 1
    for key in levels:
        # Extract ltv value/ max loan value from cell
        arr = [float(s) for s in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", row[i])]
        # Make sure this cell only has one number. Length of arr must be 1
        assert len(arr) == 1
        # If the index is 0, we have to add some zeros because the value is
        # most likely as a factor of thousands/millions
        if index == 0:
            # Let' see if we can find the factor; the factor is always at the
            # of the number
            factor = findFactor(row[i][-1])
            # If we found a factor, multiply the number by it
            if factor != -1:
                arr[0] *= factor
        # Just in case this dictionary hasn't been initialized yet
        ltv_max.setdefault(key, None)
        # Try accessing the key
        value = ltv_max[key]
        # If we didn't find the key, then this dictionary hasn't been initialized
        if value is None:
            # This dictionary hasn't been initialized yet. Create the value list
            value = [arr[0]]
        else:
            # This dictionary already has values. Append the value we have to
            # the appropriate index
            value.insert(index, arr[0])
        ltv_max[key] = value
        i += 1

def findFactor(factorC):
    # Small dictionary which holds letter as keys and the factor as 
    # values
    factors = {'k': 1000, 'm': 1000000}
    # Check to see if the parameter is a letter
    if factorC.isalpha():
        # Convert to lowercase
        factorC = factorC.lower()
        # Just in case the key is not present in dictionary
        factors.setdefault(factorC, -1)
        # Access dictionary
        factor = factors[factorC]
    return factor

def createLevels(row):
    # We skip the first index because it has no relevant information
    for i in range(1,len(row)):
        data = row[i]
        # Remove new line characters
        data.strip()
        # Find all digits in the data string
        arr = [int(s) for s in re.findall(r'\b\d+\b', data)]
        # If the arr is length 1, then the string must have specified just the lower/upper bound
        # Let's see which bound
        # lower bound
        if len(arr) == 1 and '+' in data:
            levels[(arr[0], float('inf'))] = i - 1
        # upper bound
        elif len(arr) == 1 and '-' in data:
            levels[(-float('inf'), arr[0])] = i - 1
        elif len(arr) == 2:
            # This is a boundary
            levels[(arr[0], arr[1])] = i - 1
    
def ltcRow(row):
    # Grab all numbers from the very first cell in the row
    arr = [float(s) for s in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", row[0])]
    # If length is one, the number must be representing the upper bound
    if len(arr) == 1 and 'up' in row[0]:
        ltc[(0, arr[0])] = len(ltc)
    # Specifying a bound
    elif len(arr) == 2:
        ltc[(arr[0], arr[1])] = len(ltc)

def ratesColumn(row):
    # Find all digits in the very first cell of the row
    arr = [int(s) for s in re.findall(r'\b\d+\b', row[0])]
    # Let's clean up the row:
    for i in range(1, len(row)):
        # Get rid of new line characters
        row[i] = row[i].strip()
        # Isolate number
        arr = [float(s) for s in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", row[i])]
        # This array has to be of length 0/1; in other words, each cell can only
        # have one number at most
        assert len(arr) <= 1
        # Put this number into the rates array
        if len(arr) == 1:
            rates[i - 1].append(arr[0])
        else:
            # This means that there is no valid rate for this cell entry
            # Let's fill it with -1
            rates[i - 1].append(-1)
    return rates

def statesRates(row):
    print(row)
    # First we make sure the length of this row is only 2: there should only
    # be the states in index0 and the interest rate adjustment for those states
    # in index1
    assert len(row) == 2
    # This will hold all the states
    bucket = row[0].split(',')
    # There seems to be a small issue with this number in some cases
    # Decimal point cannot be detected sometimes: if there is no decimal point,
    # then if the number is 2 digits, prefix it with a decimal point and if the
    # number is 3 digits, add a decimal point after the first digit
    if '.' not in row[1]:
        numDigits = sum(c.isdigit() for c in row[1])
        if numDigits == 2:
            row[1] = '.' + row[1]
        elif numDigits == 3:
            row[1] = row[1][0] + '.' + row[1][1:]
    adj = [float(s) for s in re.findall(r"[-+]?(?:\d*\.\d+|\d+)", row[1])]
    # Each state gets its own entry in the dictionary
    for state in bucket:
        # Strip spaces and new line characters from each state abbreviation
        state = state.strip()
        # Add an entry to the dictionary
        state_adj[state] = adj[0]

# def ineligibleStates():
#     # This table is not detected by textract. As a result, we will use tabula
#     # The assumption is that the table header will have the words 'ineligible'
#     # and 'states'
#     dfs = tabula.read_pdf("Loans.pdf", multiple_tables=True)
#     # Iterate through dataframes to find the right table
#     for df in dfs:

def get_children_ids(block):
    for rels in block.get('Relationships', []):
        if rels['Type'] == 'CHILD':
            yield from rels['Ids']

def map_blocks(blocks, block_type):
    return {
        block['Id']: block
        for block in blocks
        if block['BlockType'] == block_type
    }

# Find the interest rate/ltv/loan amount based on the housesFlipped and ltc value
def findRate(housesFlipped, ltcVal):
    index1 = -1
    index2 = -1
    rate = -1
    keyFound = None
    ltvValue = -1
    maxLoan = -1
    for key in levels:
        # Each key represents a range so we are looking for the range that
        # contains housesFlipped in the levels dictionary. The value will
        # be index1
        if housesFlipped >= key[0] and housesFlipped <= key[1]:
            keyFound = key
            index1 = levels[key]
    
    for key in ltc:
        # We do a similar search within the ltc dictionary, except we use the
        # ltcVal
        if ltcVal >= key[0] and ltcVal <= key[1]:
            index2 = ltc[key]
        
    # Now we have to make sure we found values in both dictionaries
    if index1 != -1 and index2 != -1:
        # Seems like we did
        rate = rates[index1][index2]

    # Now let's find the LTV value and the max loan; this is based on the same
    # key found in the levels dictionary
    if key is not None:
        maxLoan = ltv_max[keyFound][0]
        ltvValue = ltv_max[keyFound][1]

    print('\n')
    print("THE INTEREST RATE: " + str(rate))
    print("THE LTV VALUE: " + str(ltvValue))
    print("The MAX LOAN: " + str(maxLoan))
    

if __name__ == "__main__":
    main()