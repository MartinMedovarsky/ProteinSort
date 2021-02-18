import requests
import time
import csv
import re
import json

#Clears current itemData file.
with open("itemData.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID","name","description","imgURL","cat","subCat","price","packSize","cupPrice","cupMeasure","PPGP","PPP","PPS","veg","allergens"])

#The ID codes used within API calls
#Using categories instead of all to illiminate non-food categories
categoryIDs = ["1-E5BEE36E","1_D5A2236","1_DEB537E","1_6E4F4E4","1_39FD49C","1_ACA2FC2","1_5AF3A0A"]


#Checks if there are any more pages in the category
def pageCheck(itemCount):
    if(itemCount < 36):
        return False
    else: return True


#Parses JSON data and prepares it for adding to a database
#Calcualates values needed for the database, including price per gram of protein
def calculations(r_dict, x):
    PPGP = 0 #Price Per Gram of Protein
    PPP = 0 #Protein Per Product
    PPS = 0 #Protein Per Serve
    pContent = 0 #Protein content per 100 grams of product

    #Nutritional information string
    nutri = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["nutritionalinformation"]
    nutri = json.loads(nutri)

    #Loop finds and parses protein per 100 grams of product
    for i in range(len(nutri["Attributes"])):
        if (nutri["Attributes"][i]["Id"] == 878):
            #Removes any non numeric or decimal characters
            pContent = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            #Checks if first character is a decimal, then removes it
            if (pContent.find(".") == 0):
                pContent = pContent[1:]

            print("Protein per 100g: " + str(nutri["Attributes"][i]["Value"]))
            print("pContent: " + str(pContent))

        if (nutri["Attributes"][i]["Id"] == 882):
            PPS = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            if (PPS.find(".") == 0):
                PPS = PPS[1:]

            print("PPS: " + str(PPS))

    price = r_dict["Bundles"][x]["Products"][0]["Price"]
    weight = r_dict["Bundles"][x]["Products"][0]["PackageSize"]

    cupPrice = r_dict["Bundles"][x]["Products"][0]["CupPrice"]
    cupMeasure = r_dict["Bundles"][x]["Products"][0]["CupMeasure"]

    if cupMeasure == "1KG" or cupMeasure == "1L":
        #PPGP = (cupPrice / cupMeasure) / 10
        print("1KG or 1L")
    elif cupMeasure == "100G":
        print("100G")
    elif cupMeasure == "1EA":
        print("1EA")
        #Will need to use unit weight in grams here
        #Neither unit weight in grams or cup measure will work for everything unfortunately.
    else: print("UH OH")

    return True

#Adds data and adds item to database
def addItem(r_dict, x):

    calculations(r_dict, x)

    with open("itemData.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["test","test","test","test","test","test","test","test","test","test","test","test","test","test","test"])


#Main logic loop
#Outer loop cycles through categories
for ID in categoryIDs:
    morePages = True
    currentPage = 1

    while morePages == True:

        payload = {"categoryId":ID,
                    "pageNumber":currentPage,
                    "pageSize":"36",
                    "url":"a",
                    "formatObject":"{}"}

        r = requests.post('https://www.woolworths.com.au/apis/ui/browse/category', data=payload)
        r_dict = r.json()

        itemCount = len(r_dict["Bundles"])

        #print(r_dict)
        #print(r_dict["TotalRecordCount"])

        #print("First Item name " + r_dict["Bundles"][0]["Name"])
        print("Page number " + str(currentPage))

        for x in range(itemCount):
            print(r_dict["Bundles"][x]["Name"])
            info = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["nutritionalinformation"]
            
            #Checks if the selected product contains protein nutritional information
            if info is None or info.find("Protein") == -1 or info.find('"Protein Quantity Per 100g - Total - NIP\",\"Value\":\"0.0g\"') > 0:
                print("No protein")
            else:
                print("Protein!")
                addItem(r_dict, x)

        currentPage += 1
        morePages = pageCheck(itemCount) 
        time.sleep(3)
    