from bs4 import BeautifulSoup

for i in range(1,5):
    # Read the HTML content from the file
    with open(f'scrr{i}.html', 'r') as file:
        html_content = file.read()

    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all the div elements with class "_a6-p"
    rows = soup.find_all('div', class_='x1rg5ohu')

    # Open a file to write the names
    with open('scrr.txt', 'r+') as output_file:
        # Extract the name of the person from each row
        for row in rows:
            name_element = row.find('a')  # Find the 'a' element within the row
            if name_element:  # Check if the name element exists
                name = name_element.get('href')[1:-1]  # Extract the text and strip any extra whitespace
                output_file.seek(0)  # Move the cursor to the beginning of the file
                names = output_file.readlines()  # Read all lines from the file
                if name + '\n' not in names:  # Check if the name is not already in the file
                    output_file.write(name + '\n')  # Write the name to the file
