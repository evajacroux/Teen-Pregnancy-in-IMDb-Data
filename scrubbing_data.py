"Scrub IMDb website to create data set of titles tagged with keyword 'teenage-pregnancy'"
# Call website to scrub (notice it is page 1 of search results, shown by page=1 in url)
from requests import get
url = "https://www.imdb.com/search/keyword/?keywords=teenage-pregnancy&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=1"
response = get(url)
print(response.text[:500])

# Import Python module Beautiful Soup to parse HTML
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, "html.parser")
type(html_soup)

# Find all movies on page of IMDb
movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-detail')
print(type(movie_containers))
print(len(movie_containers))

# Get first movie by indexing first position in movie_containers
first_movie = movie_containers[0]

"Parse desired information from HTML. This code parses movie title and tconst (unique identifier) to join into" 
"public IMDb data sets."

# Within the first_movie HTML text, get lines tagged <h3>. Amongst those, get line tagged <a>. Convert to text.
first_name = first_movie.h3.a.text
print(first_name)

# Within the first_movie HTML text, get lines tagged with <div>. Amongst those, get line with class "lister-item-image ribbonize"
first_tconst = first_movie.find('div', class_ = 'lister-item-image ribbonize')
first_tconst = first_tconst['data-tconst']
print(first_tconst)

"Create for loop to parse all movies on in search of keywork 'teenage pregnancy'"

# Create lists for variables: movie title (name), and unique identifier (tconst)
names = []
tconst = []

# Create list for number of pages (as strings) to iterate through (there are 10 pages)
pages = [str(i) for i in range(1,11)]

# Iterate through list pages (numbers 1-10), and add it to the end of the url as a string
for page in pages:
    url = "https://www.imdb.com/search/keyword/?keywords=teenage-pregnancy&ref_=kw_nxt&sort=moviemeter,asc&mode=detail&page=" + page
    response = get(url)

    # Call each page from generated url above
    html_soup = BeautifulSoup(response.text, "html.parser")

    # Parse movies from the page
    movie_containers = html_soup.find_all('div', class_ = 'lister-item mode-detail')

    # Iterate through each movie on the page and parse movie tite (name) and unique identifier (tconst)
    # Append these variables to their respective lists
    for container in movie_containers:
        name = container.h3.a.text
        names.append(name)
        id = container.find('div', class_ = 'lister-item-image ribbonize')
        id = id['data-tconst']
        tconst.append(id)

"Create and export csv file"

# Create dataframe using Pandas from lists 'names' and 'tconst'
import pandas as pd
test_df = pd.DataFrame({'movie': names,
'id': tconst
})
print(test_df.info)

# Write dataframe to csv file
test_df.to_csv("teen_pregnant_media.csv", header = ["primary title", "const"])