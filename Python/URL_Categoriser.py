import requests
from urllib.parse import urlparse
import csv

# Function to extract domain from URL
def extract_domain(url, domain_data):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri).replace('www.', '')
    if 'www.' + domain in domain_data:
        return 'www.' + domain
    return domain

def get_all_domains(api_url):
    all_domains = {}
    page_url = api_url  # Start with the initial API URL
    
    while page_url:
        response = requests.get(page_url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            # Update all_domains with new data
            all_domains.update({item['domain_name']: item['category_code'] for item in results})
            page_url = data.get('next')  
        else:
            print(f'Failed to fetch page: {page_url}')
            break
    
    return all_domains

# Start the pagination process
categorised_domains = get_all_domains('https://api.ooni.io/api/_/domains')

# Load list of domains to be categorised
with open('URLlist.txt', 'r') as file:
    your_domains = [line.strip() for line in file]

normalised_domains = [extract_domain(url, categorised_domains) for url in your_domains]


# Create or open a file to write the results

with open('categorised_domains.csv', 'w', newline='') as csvfile:
    fieldnames = ['domain', 'category']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    # Write the header
    writer.writeheader()

    # Write the domain and its category as rows in the CSV
    for domain in normalised_domains:
        # Use the normalised domain to get the category
        category = categorised_domains.get(domain, 'Unknown')  # Default to 'Unknown' if not found
        writer.writerow({'domain': 'https://' + domain, 'category': category})


print('The domain categories have been written to categorised_domains.csv')
