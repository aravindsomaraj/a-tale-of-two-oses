from bs4 import BeautifulSoup

# Read the HTML content from the file
with open('following.html', 'r') as file:
    html_content = file.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')

# Find all the div elements with class "_a6-p"
rows = soup.find_all('div', class_='_a6-p')

# Open a file to write the names
with open('following.txt', 'w') as output_file:
    # Extract the name of the person from each row
    for row in rows:
        name_element = row.find('a')  # Find the 'a' element within the row
        if name_element:  # Check if the name element exists
            name = name_element.text.strip()  # Extract the text and strip any extra whitespace
            output_file.write(name + '\n')  # Write the name to the file
