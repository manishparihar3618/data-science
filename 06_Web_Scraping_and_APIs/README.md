# Web Scraping with Beautiful Soup

## What is Web Scraping?

Web scraping is the process of extracting data from websites automatically using Python.

**Common ML Uses**

* Dataset collection
* Price prediction
* Sentiment analysis
* News scraping
* Job market analysis

## Required Libraries

```python
import requests
from bs4 import BeautifulSoup
```

Install:

```bash
pip install requests beautifulsoup4 lxml
```

---

## Basic Workflow

```
URL
 ↓
requests.get()
 ↓
HTML Response
 ↓
BeautifulSoup()
 ↓
Find Elements
 ↓
Extract Data
 ↓
Store in CSV / Database
```

---

## Basic Example

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title.text)
```

---

## Common Methods

```python
soup.find("tag")           # First matching element
soup.find_all("tag")       # All matching elements
soup.select(".class")      # CSS selector
soup.select_one("#id")     # Single CSS selector

tag.text                   # Get text
tag.get("href")            # Get attribute
```

---

## Common Status Codes

* **200** → Success
* **403** → Forbidden
* **404** → Not Found
* **500** → Server Error

---

## Best Practices

* Use a **User-Agent** header.
* Check `response.status_code`.
* Respect `robots.txt` and website policies.
* Save extracted data using **Pandas**.

---

## Output Example

```
Website
   ↓
Requests
   ↓
BeautifulSoup
   ↓
Extract Data
   ↓
CSV / Excel / Database
```
