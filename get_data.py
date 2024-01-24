from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_row_state(row):
    """
    Extracts the state from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - State string if found, 'Error - get_row_state' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-fraud-state-administrative-area'})
        state_string = items.text
        return state_string[5:]
    except:
        return 'Error - get_row_state'
    
def get_row_year(row):
    """
    Extracts the year of disposition from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Year string if found, 'Error - get_row_year' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-year-of-disposition'})
        year_string = items.text
        return year_string[4:]
    except:
        return 'Error - get_row_year'

def get_row_name(row):
    """
    Extracts the name from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Name string if found, 'Error - get_row_name' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-name'})
        name_string = items.text
        return name_string[4:]
    except:
        return 'Error - get_row_name'

def get_row_case_type(row):
    """
    Extracts the case type from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Case type string if found, 'Error - get_row_case_type' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-case-type'})
        case_type_string = items.text
        return case_type_string[9:]
    except:
        return 'Error - get_row_case_type'

def get_row_fraud_type(row):
    """
    Extracts the fraud type from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Fraud type string if found, 'Error - get_row_fraud_type' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-fraud-type'})
        fraud_type_string = items.text
        return fraud_type_string[10:]
    except:
        return 'Error - get_row_fraud_type'

def get_row_outcomes(extra, index):
    """
    Extracts the outcomes from a given row.

    Parameters:
    - extra: BeautifulSoup object representing the extra row in the HTML table
    - index: Index of the row in the extra rows

    Returns:
    - Outcomes string if found, 'Error - get_row_outcomes' otherwise
    """
    try:
        count = 0
        for row in extra:
            if count == index:
                outcomes = row.find('p', attrs={'class':'outcomes'})
                return str(outcomes.text.strip())
            count = count + 1
    except:
        return 'Error - get_row_outcomes'

def get_row_source(extra, index):
    """
    Extracts the sources from a given row.

    Parameters:
    - extra: BeautifulSoup object representing the extra row in the HTML table
    - index: Index of the row in the extra rows

    Returns:
    - Cleaned sources string if found, 'Error - get_row_source' otherwise
    """
    try:
        count = 0
        for row in extra:
            if count == index:
                sources = row.find('p', attrs={'class':'sources'})
                clean1 = str(repr(sources.text.strip()))
                clean2 = clean1.replace('\\n', '')
                clean3 = clean2.replace('\\t', '')
                clean4 = clean3.replace('\\r', '')
                clean5 = clean4.replace('  ', '')
                clean8 = clean5.replace('Source: ', '')
                clean9 = clean8.replace(',https', ', https')
                clean10 = clean9.replace(',herit.ag', ', herit.ag')
                return clean10
            count = count + 1
    except:
        return 'Error - get_row_source'

def run():
    """
    Scrapes and prints information about voter fraud cases from a website.

    This function sends a request to a website, downloads the HTML contents,
    parses the HTML using BeautifulSoup, and extracts information about voter
    fraud cases from the parsed HTML. It then prints the extracted information.

    Note: This function assumes that the required modules (BeautifulSoup and requests)
    have been imported.

    Returns:
    None
    """
    # Request to website and download HTML contents
    url = 'https://www.heritage.org/voterfraud-print/search'
    req = requests.get(url)
    content = req.text

    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(content, 'html.parser')

    # Get the table
    table = soup.find_all('div', attrs={'class': 'views-row'})
    extra = soup.find_all('div', attrs={'class': 'extra-row'})

    # Initialize count
    count = 0

    # Remove extra records
    extra_records = 14

    # Create a dataframe
    df = pd.DataFrame(columns=['State', 'Year', 'Name', 'Case Type', 'Fraud Type', 'Outcomes', 'Source'])

    # Print each row
    for row in table[1:(len(table)-extra_records)]:
        state = get_row_state(row)
        year = get_row_year(row)
        name = get_row_name(row)
        case_type = get_row_case_type(row)
        fraud_type = get_row_fraud_type(row)
        outcomes = get_row_outcomes(extra, count)
        source = get_row_source(extra, count)

        df = df._append({
            'State': state, 
            'Year': year, 
            'Name': name, 
            'Case Type': case_type, 
            'Fraud Type': fraud_type, 
            'Outcomes': outcomes, 
            'Source': source}, 
            ignore_index=True)

        print('State: ', state)
        print('Year: ', year)
        print('Name: ', name)
        print('Case Type: ', case_type)
        print('Fraud Type: ', fraud_type)
        print('Outcome: ', outcomes)
        print('Source: ', source)
        print('-----------------')
        count = count + 1

    # Print dataframe
    print(df.head())

    # Save dataframe to csv
    df.to_csv('voter_fraud_cases.csv')

run()