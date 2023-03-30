import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from bs4 import BeautifulSoup

# define the Google Sheet credentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)

# open the Google Sheet and select the first worksheet
sheet = client.open('Colleges').sheet1

# loop through each row of the Google Sheet
for i in range(2, sheet.row_count + 1):
    # get the website URL of the college
    website = sheet.cell(i, 2).value
    
    # fetch the HTML content of the website and handle any exceptions
    try:
        response = requests.get(website)
    except requests.exceptions.RequestException as e:
        sheet.update_cell(i, 3, 'Error: ' + str(e))
        sheet.update_cell(i, 4, 'Error: ' + str(e))
        continue
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # find the address of the college
    address_element = soup.find('adr')
    if address_element is not None:
        address = address_element.text.strip()
    else:
        address = ''
    
    # find the name of the principal of the college
    try:
        principal_element = soup.find('name').find_previous('td')
        principal = principal_element.text.strip()
    except:
        principal = ''
    
    # update the Google Sheet with the address and the name of the principal
    sheet.update_cell(i, 3, address)
    sheet.update_cell(i, 4, principal)
