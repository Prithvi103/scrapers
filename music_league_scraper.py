

import requests
from bs4 import BeautifulSoup

# Function to search for specific terms and extract links from the resulting pages
def search_and_extract_links(url, search_terms):
    # Search for the terms in the content
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content = soup.get_text()
    # If all terms are found, extract links from the page
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('https://www.tamil2lyrics.com'):
            links.append(href)
    return links

# Example usage
search_terms = [' january ', ' february ', ' march ', ' april ', ' may ', ' june ', ' july ', ' august ', ' september ', ' october ', ' november ', ' december ', ' vaigasi ', ' margazhi ', ' marghazhi ', ' karthigai ', ' chithirai ' ]
starting_url = 'https://www.tamil2lyrics.com/'

def check_for_terms(link, search_terms):
    if "/lyrics/" in link:
        # Make a GET request to the link
        response = requests.get(link)
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get the text content of the page
        # text = soup.get_text()
        content = soup.find('div', {'class': 'mainlyricscontent'}).get_text().strip().lower()
        # Check if any of the search terms are in the text content
        for term in search_terms:
            if term.lower() in content.lower():
                return True
        
        # If no search terms were found, return False
    return False

# Search for the terms and extract links from the resulting pages
visited_urls = set()
links_to_visit = [starting_url]
while links_to_visit:
    current_url = links_to_visit.pop(0)
    if current_url not in visited_urls:
        visited_urls.add(current_url)
        links = search_and_extract_links(current_url, search_terms)
        if check_for_terms(current_url, search_terms):
            with open('links.txt', 'a') as f:
                f.writelines('\n'.join(links) + '\n')
        links_to_visit.extend(link for link in links if link not in visited_urls)
