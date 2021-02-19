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

    #These are used for products using price per EACH
    price = r_dict["Bundles"][x]["Products"][0]["Price"]
    weight = r_dict["Bundles"][x]["Products"][0]["UnitWeightInGrams"] #This weight is accurate for EA products

    #These are used for products using standard price per 100g or price per KG
    cupPrice = r_dict["Bundles"][x]["Products"][0]["CupPrice"]
    cupMeasure = r_dict["Bundles"][x]["Products"][0]["CupMeasure"]
    altWeight = r_dict["Bundles"][x]["Products"][0]["PackageSize"] #This weight is accurate for packaged products

    #Parses altWeight to be an int representing grams
    if (altWeight.find("KG") != -1 or altWeight.find("kg") != -1):
        altWeight = int(re.sub('[^0-9.]','', altWeight))
        altWeight = altWeight * 1000
        print("Package Size: " + str(altWeight) + "g")
    elif (altWeight.find("G") != -1 or altWeight.find("g") != -1):
        altWeight = int(re.sub('[^0-9.]','', altWeight))
        print("Package Size: " + str(altWeight) + "g")
    else: print("Unknown Package Size")


    #Loop finds and parses protein per 100 grams of product
    for i in range(len(nutri["Attributes"])):
        if (nutri["Attributes"][i]["Id"] == 878):
            #Removes any non numeric or decimal characters
            pContent = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            #Checks if first character is a decimal, then removes it
            if (pContent.find(".") == 0):
                pContent = pContent[1:]

            pContent = float(pContent)

            print("Protein per 100g: " + str(nutri["Attributes"][i]["Value"]))
            print("pContent: " + str(pContent))

        if (nutri["Attributes"][i]["Id"] == 882):
            PPS = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            if (PPS.find(".") == 0):
                PPS = PPS[1:]

            print("PPS: " + str(PPS))

    #
    if cupMeasure == "1KG" or cupMeasure == "1L":
        print("1KG or 1L")
        print("Price per 100g: " + str(cupPrice / 10))
        PPGP = (cupPrice / 10) / pContent
    elif cupMeasure == "100G":
        print("100G")
        print("Price per 100g: " + str(cupPrice))
        PPGP = cupPrice / pContent
    elif cupMeasure == "1EA" or cupMeasure == "0":
        print("1EA")
        print("Price per 100g: " + str((100 / weight) * price))
        PPGP = ((100 / weight) * price) / pContent 
    else: print("UH OH")
    print("Price per gram of protein: " + str(PPGP) + "\n")

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
    