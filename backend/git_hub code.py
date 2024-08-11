from requests_html import HTMLSession
import requests
from lxml import etree
from urllib.parse import unquote
import json

def search(query):
    result = []
    PAGINATION = 0

    while True:
        session = HTMLSession()
        url = 'https://www.google.com/localservices/prolist?hl=en&ssta=1&q='+query+'&oq='+query+'&src=2&lci='+str(PAGINATION)
        print(url)
        # r = session.get(url)
        # r.html.render(timeout=20)
        r=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        html=etree.HTML(r.text)
        print(html.cssselect('#yDmH0d > script:nth-child(12)')[0].text)
        data_script = html.cssselect('#yDmH0d > script:nth-child(12)')[0].text.replace("AF_initDataCallback(","").replace("'","").replace("\n","")[:-2]
        data_script = data_script.replace("{key:","{\"key\":").replace(", hash:",", \"hash\":").replace(", data:",", \"data\":").replace(", sideChannel:",", \"sideChannel\":")
        data_script = data_script.replace("\"key\": ds:","\"key\": \"ds: ").replace(", \"hash\":","\",\"hash\":")
        data_script = json.loads(data_script)

        placesData = data_script["data"][1][0]

        try:
            for i in range(0,len(placesData)):
                obj = {
                    "id": placesData[i][21][0][1][4],
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
                    None

                try:
                    obj["domain"] = placesData[i][10][1][1]
                    obj["url"] = placesData[i][10][1][0]
                except TypeError:
                    None

                try:
                    obj["address"] = unquote(placesData[i][10][8][0][2]).split("&daddr=")[1].replace("+"," ")
                except:
                    None

                try:
                    obj["coor"] = str(placesData[i][19][0])+","+str(placesData[i][19][1])
                except:
                    None

                try:
                    obj["stars"] = placesData[i][21][3][0]
                    obj["reviews"] = placesData[i][21][3][2]
                except:
                    None

                result.append(obj)
        except TypeError:
            session.close()
            PAGINATION = 0
            break

        if(len(placesData) < 20):
            session.close()
            PAGINATION = 0
            break
        else:
            PAGINATION += len(placesData)

    return result
if __name__=="__main__":
    res=search("gift shop in chennai")
    with open("final.json", 'w') as f:
        json.dump(res, f)
    print(len(res))