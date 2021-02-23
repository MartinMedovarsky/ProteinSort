import requests
import time
import csv
import re
import json

#Clears current itemData file.
with open("itemData.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID","name","description","imgURL","imgURLMed","dep","cat","price","packSize","cupPrice","cupMeasure","servings","pContent","PPGP","PPS"])

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
    PPS = 0 #Protein Per Serve
    pContent = 0 #Protein content per 100 grams of product
    servings = "0" #Servings per package

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

    #Parses altWeight to be an float representing grams
    #Checks that the weight isnt variable or minimum eg. 1.4 kg - 2.4 kg
    if altWeight.find("-") == -1 and altWeight.find("min") == -1:
        if (altWeight.find("KG") != -1 or altWeight.find("kg") != -1):
            altWeight = altWeight.lower()
            print(altWeight)
            if (altWeight == "per kg"):
                altWeight = 1000
            else:
                altWeight = float(re.sub('[^0-9.]','', altWeight))
                altWeight = altWeight * 1000
            print("Package Size: " + str(altWeight) + "g")
        elif (altWeight.find("G") != -1 or altWeight.find("g") != -1):
            altWeight = float(re.sub('[^0-9.]','', altWeight))
            print("Package Size: " + str(altWeight) + "g")
        else: print("Unknown Package Size")
    else: altWeight = "n/a"


    #Loop finds and parses certain nutritional information
    for i in range(len(nutri["Attributes"])):
        if (nutri["Attributes"][i]["Id"] == 878):
            #Removes any non numeric or decimal characters
            pContent = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            #Checks if first character is a decimal, then removes it
            if (pContent.find(".") == 0):
                pContent = pContent[1:]

            try:
                pContent = float(pContent)
            except:
                print("Issue with protein content, likely multiple items")
                return None

            print("Protein per 100g: " + str(nutri["Attributes"][i]["Value"]))
            print("pContent: " + str(pContent))

        if (nutri["Attributes"][i]["Id"] == 882):
            PPS = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            if (PPS.find(".") == 0):
                PPS = PPS[1:]

            try:
                PPS = float(PPS)
            except:
                print("Issue with protein serving")
                return None

            print("PPS: " + str(PPS))

        if (nutri["Attributes"][i]["Id"] == 544):
            servings = nutri["Attributes"][i]["Value"]
            if servings is not None:
                servings = servings.lower()
                if (servings.find("g") == -1):
                    print("Servings: " + str(servings))
                else: servings = 0

    #Calculates protein per product if possible

    #Calculates Price Per Gram of Protein
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
        print(weight)
        print(price)
        print("Price per 100g: " + str((100 / weight) * price))
        PPGP = ((100 / weight) * price) / pContent 
    else: print("UH OH")
    print("Price per gram of protein: " + str(PPGP) + "\n")

    return PPGP, PPS, pContent, servings, cupPrice

#Adds data and adds item to database
def addItem(r_dict, x):
    
    try: 
        PPGP, PPS, pContent, servings, cupPrice = calculations(r_dict, x)
    except:
        return

    print ("PPGP: " + str(PPGP) + " PPS: " + str(PPS) + " pContent: " + str(pContent) + " servings: " + str(servings))

    ID = r_dict["Bundles"][x]["Products"][0]["Stockcode"] #used as ID and for URL
    name = r_dict["Bundles"][x]["Name"]
    description = r_dict["Bundles"][x]["Products"][0]["RichDescription"]
    imgURL = r_dict["Bundles"][x]["Products"][0]["LargeImageFile"]
    imgURLMed = r_dict["Bundles"][x]["Products"][0]["MediumImageFile"]
    dep = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["piesdepartmentnamesjson"][1:-1]
    cat = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["piescategorynamesjson"][1:-1]
    price = r_dict["Bundles"][x]["Products"][0]["Price"]
    packSize = r_dict["Bundles"][x]["Products"][0]["PackageSize"]
    cupMeasure = r_dict["Bundles"][x]["Products"][0]["CupMeasure"]

    with open("itemData.csv", "a", newline="") as file:
        writer = csv.writer(file)

        #Catches any outliers. Often to do with strange text encoding
        try:
            writer.writerow([ID, name, description, imgURL, imgURLMed, dep, cat, price, packSize, cupPrice, cupMeasure, servings, pContent, PPGP, PPS])
        except:
            return

#Main logic loop
#Outer loop cycles through categories
totalItems = 0 #Used to count total entries, even discarded ones
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

        #Amount of item in the api request. Normally 32 but can be lower.
        itemCount = len(r_dict["Bundles"])

        print("Page number " + str(currentPage))

        for x in range(itemCount):
            totalItems += 1
            print(totalItems)

            print(r_dict["Bundles"][x]["Name"])
            info = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["nutritionalinformation"]
            price = r_dict["Bundles"][x]["Products"][0]["Price"]
            
            #Checks if the selected product contains protein nutritional information
            #Could use array and loop to get rid of some of these elifs
            conditions = ["\"0", "null", "\"Approx. 0", "\"Approx.0", "\"<0"]

            #containsP = True

            #for cond in conditions:
            #    if info.find('Protein Quantity Per 100g - Total - NIP\",\"Value\":' + cond) > 0:
            #        print("No protein \n")
            #        containsP = False

            if info is None or info.find("Protein Quantity Per 100g") == -1 or info.find('"Protein Quantity Per 100g - Total - NIP\",\"Value\":\"0') > 0:
                print("No protein \n")
            elif info.find("Protein Quantity Per 100g - Total - NIP\",\"Value\":null") > 0:
                print("No protein \n")
            elif info.find('"Protein Quantity Per 100g - Total - NIP\",\"Value\":\"Approx. 0') > 0:
                print("No protein \n")
            elif info.find('"Protein Quantity Per 100g - Total - NIP\",\"Value\":\"Approx.0') > 0:
                print("No protein \n")
            elif info.find('"Protein Quantity Per 100g - Total - NIP\",\"Value\":\"<0') > 0:
                print("No protein \n")
            elif price is None:
                print("No price \n")
            else:
                print("Protein!")
                addItem(r_dict, x)

        currentPage += 1
        morePages = pageCheck(itemCount) 
        time.sleep(2)
    