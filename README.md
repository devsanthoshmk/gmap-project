# Gmap Vigilante: Google Maps scraping project

Gmap Vigilante is a Google Maps scraping project and Python places extraction tool that collects local business data into an Excel spreadsheet.

The application queries Google Local Services, parses business listings from embedded page script data, and outputs structured local business data records. The Python places extraction pipeline handles pagination in increments of 20 results, removes duplicate place entries, and exports contact and location fields without requiring official API keys.

## Architecture

The system consists of four primary components:

1. Web server: A Flask application in app.py handles client routing, receives search queries, and streams generated spreadsheets to the client.
2. Scraper module: backend/final.py issues HTTP GET requests to the Google Local Services endpoint, locates the data payload inside the page script element, and parses the JSON structure.
3. Spreadsheet generator: openpyxl builds an in-memory workbook using BytesIO, populates business records, configures column widths, and injects Google Maps hyperlink formulas.
4. Client interface: frontend/index.html and frontend/assets/scripts/index.js present a search interface built with Vue 2 and Bootstrap 5 that initiates queries and downloads the resulting file.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/devsanthoshmk/gmap-project.git
cd gmap-project
```

2. Install the required Python packages:

```bash
pip install flask requests lxml cssselect openpyxl pandas requests-html
```

3. Verify Python 3.8 or higher is installed.

## Usage

1. Start the Flask application:

```bash
python app.py
```

2. Open a browser and navigate to http://127.0.0.1:5000/.

3. Enter a search query such as "gift shop in chennai" into the search field and press Enter.

4. The server queries Google Local Services, collects places data, and builds the spreadsheet. When processing completes, click Download to save the Excel file.

5. You can also request data directly through curl:

```bash
curl -o results.xlsx "http://127.0.0.1:5000/download?query=gift+shop+in+chennai"
```

## Configuration

- Network port: app.py runs on port 5000 by default. Modify the app.run call in app.py to change the host or port.
- User agent: backend/final.py defines the User-Agent header in the requests call to avoid request rejections.
- Pagination step: The scraper requests 20 records per batch using the lci URL parameter until it detects duplicate records or receives an empty page.
- Excel output: backend/final.py configures column widths for the 7 exported fields: NAME, CATEGORY, REVIEW_COUNT, STARS, PHONE NO., ADDRESS, and LINKS.
