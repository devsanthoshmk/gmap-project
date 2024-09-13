import asyncio
import aiohttp
from lxml import etree
from urllib.parse import unquote
import json
from time import time

seen = []
run=True
async def pagination():
    page = 0
    while True:
        yield page
        page += 20

async def fetch_page(session, url):
  try:
    async with session.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }) as response:
        html = etree.HTML(await response.text())
        data_script = html.cssselect('#yDmH0d > script:nth-child(12)')[0].text.replace("AF_initDataCallback(","").replace("'","").replace("\n","")[:-2]
        data_script = data_script.replace("{key:","{\"key\":").replace(", hash:",", \"hash\":").replace(", data:",", \"data\":").replace(", sideChannel:",", \"sideChannel\":")
        data_script = data_script.replace("\"key\": ds:","\"key\": \"ds: ").replace(", \"hash\":","\",\"hash\":")
        data_script = json.loads(data_script)

        placesData = data_script["data"][1][0]
        result = []

        for i in range(len(placesData)):
            id = placesData[i][21][0][1][4]
            if id not in seen:
                seen.append(id)
            else:
                break

            obj = {
                "id": id,
                "title": placesData[i][10][5][1],
                "category": placesData[i][21][9],
                "address": "",
                "phoneNumber": "",
                "completePhoneNumber": "",
                "domain": "",
                "url": "",
                "coor": "",
                "stars": "",
                "reviews": ""
            }

            try:
                obj["phoneNumber"] = placesData[i][10][0][0][1][0][0]
                obj["completePhoneNumber"] = placesData[i][10][0][0][1][1][0]
            except TypeError:
                pass

            try:
                obj["domain"] = placesData[i][10][1][1]
                obj["url"] = placesData[i][10][1][0]
            except TypeError:
                pass

            try:
                obj["address"] = unquote(placesData[i][10][8][0][2]).split("&daddr=")[1].replace("+"," ")
            except:
                pass

            try:
                obj["coor"] = str(placesData[i][19][0]) + "," + str(placesData[i][19][1])
            except:
                pass

            try:
                obj["stars"] = placesData[i][21][3][0]
                obj["reviews"] = placesData[i][21][3][2]
            except:
                pass

            result.append(obj)

        return result
  except:
      global run
      run=False

async def search(query):
    results = []
    async with aiohttp.ClientSession() as session:
        async for page in pagination():
            url = f'https://www.google.com/localservices/prolist?hl=en&ssta=1&q={query}&oq={query}&src=2&lci={page}'
            if run:
                result = await fetch_page(session, url)
                if result:
                    results.append(result)
                else:
                    break  # Stop if no new results are found
            else:
                return results

    with open("./backend/test_pagination.json", 'w') as f:
        json.dump(results, f)

    return results

# Usage example
st = time()
query = "restaurants in New York"
asyncio.run(search(query))
print(time() - st)
