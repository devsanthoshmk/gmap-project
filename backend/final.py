from requests_html import HTMLSession
import requests
from lxml import etree
from urllib.parse import unquote
import json

from pandas import DataFrame
from openpyxl import Workbook
from io import BytesIO

import time
t1=time.time()

def search(query):
    result = []
    PAGINATION = 0
    seen=[]
    while True:
        url = 'https://www.google.com/localservices/prolist?hl=en&ssta=1&q='+query+'&oq='+query+'&src=2&lci='+str(PAGINATION)
        # print(url)

        r=requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
        html=etree.HTML(r.text)
        # print(html.cssselect('#yDmH0d > script:nth-child(12)')[0].text)
        data_script = html.cssselect('#yDmH0d > script:nth-child(12)')[0].text.replace("AF_initDataCallback(","").replace("'","").replace("\n","")[:-2]
        data_script = data_script.replace("{key:","{\"key\":").replace(", hash:",", \"hash\":").replace(", data:",", \"data\":").replace(", sideChannel:",", \"sideChannel\":")
        data_script = data_script.replace("\"key\": ds:","\"key\": \"ds: ").replace(", \"hash\":","\",\"hash\":")
        data_script = json.loads(data_script)

        placesData = data_script["data"][1][0]
        print(PAGINATION)
        try:
            for i in range(0,len(placesData)):
                id=placesData[i][21][0][1][4]
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

            PAGINATION += 20
        except TypeError:
            break

        # if(len(placesData) < 20):
        #     session.close()
        #     PAGINATION = 0
        #     break
        # else:
        #     PAGINATION += len(placesData)

    # with open("./backend/test_pagination.json", 'w') as f:
    #     json.dump(data_script["data"], f)
    # print()
    # # return result
    full_list=[["NAME","CATEGORY","REVIEW_COUNT","STARS","PHONE NO.","ADDRESS","LINKS"]]
    for i in result:
        # try:
            # status=i['state']
            # if "Open" in status or "Closed" in status:        STATE/STATUS IS NOT FOUND BY THIS METHOD BUT CAN USING RAPID API
            #     Status="Functioning"
            # else:
            #     Status="Not Sure"
        # except (KeyError,TypeError):
        #     Status=""
        full_list.append([i['title'],i['category'],i['reviews'],i['stars'],i['completePhoneNumber'],i['address'],f'=HYPERLINK("https://www.google.com/maps/place/?q=place_id:{i["id"]}", "Click here")'   ])
        
      
    wb = Workbook()
    excel_buffer = BytesIO()
    ws = wb.active

    for row in full_list:
        ws.append(row)

    # Adjust column widths
    column_widths = [40,20, 13, 23, 8, 17, 50, 10]
    for col_num, width in enumerate(column_widths, start=1):
        col_letter = ws.cell(row=1, column=col_num).column_letter
        ws.column_dimensions[col_letter].width = width

    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer


    
if __name__=="__main__":
    search("gift shop in chennai")
    
    ''' To test without writing excel...'''
    # with open("./backend/final.json", 'w') as f:
    #     json.dump(res, f)
    # def remove_duplicates(data, key):
    #     seen = set()
    #     unique_data = []
    #     for item in data:
    #         # Extract the value of the specified key
    #         value = item[key]
    #         # If the value hasn't been seen before, add it to the unique_data list
    #         if value not in seen:
    #             unique_data.append(item)
    #             seen.add(value)
    #     return unique_data
    # print(res[0])
    # print(len(res))
    # print(len(remove_duplicates(res,"id")))
    # print((time.time()-t1))
    