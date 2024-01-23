from bs4 import BeautifulSoup
import requests

def get_row_state(row):
    """
    Extracts the state from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - State string if found, 'N/A' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-fraud-state-administrative-area'})
        state_string = items.text
        return state_string[5:]
    except:
        return 'N/A'
    
def get_row_year(row):
    """
    Extracts the year of disposition from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Year string if found, 'N/A' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-year-of-disposition'})
        year_string = items.text
        return year_string[4:]
    except:
        return 'N/A'

def get_row_name(row):
    """
    Extracts the name from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Name string if found, 'N/A' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-name'})
        name_string = items.text
        return name_string[4:]
    except:
        return 'N/A'

def get_row_case_type(row):
    """
    Extracts the case type from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Case type string if found, 'N/A' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-case-type'})
        case_type_string = items.text
        return case_type_string[9:]
    except:
        return 'N/A'

def get_row_fraud_type(row):
    """
    Extracts the fraud type from a given row.

    Parameters:
    - row: BeautifulSoup object representing a row in the HTML table

    Returns:
    - Fraud type string if found, 'N/A' otherwise
    """
    try:
        items = row.find('span', attrs={'class': 'views-field-field-fraud-type'})
        fraud_type_string = items.text
        return fraud_type_string[10:]
    except:
        return 'N/A'

def get_row_outcomes(extra, count2):
    """
    Extracts the outcomes from a given row.

    Parameters:
    - extra: BeautifulSoup object representing the extra row in the HTML table
    - name: Name of the row
    - count2: Index of the row in the extra rows

    Returns:
    - Outcomes string if found, 'N/A' otherwise
    """
    try:
        count = 0
        for row in extra:
            if count == count2:
                outcomes = row.find('p', attrs={'class':'outcomes'})
                return str(outcomes.text.strip())
            count = count + 1
    except:
        return 'N/A - GetRowSource Error'

def get_row_source(extra, count2):
    """
    Extracts the sources from a given row.

    Parameters:
    - extra: BeautifulSoup object representing the extra row in the HTML table
    - count2: Index of the row in the extra rows

    Returns:
    - Cleaned sources string if found, 'N/A - GetRowSource Error' otherwise
    """
    try:
        count = 0
        for row in extra:
            if count == count2:
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
        return 'N/A - GetRowSource Error'


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

    count = 0

    # Print each row
    for row in table[1:2000]:
        print('State: ', get_row_state(row))
        print('Year: ', get_row_year(row))
        print('Name: ', get_row_name(row))
        print('Case Type: ', get_row_case_type(row))
        print('Fraud Type: ', get_row_fraud_type(row))
        print('Outcome: ', get_row_outcomes(extra, count))
        print('Source: ', get_row_source(extra, count))
        print('-----------------')
        count = count + 1

run()