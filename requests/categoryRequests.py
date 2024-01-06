import requests
import time
import re
import json
import mysql.connector

#Connecting to mysql database
conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'password',
    database = 'proteinsort')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS itemDATA (
                ID INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                imgURL TEXT,
                imgURLMed TEXT,
                dep TEXT,
                cat TEXT,
                price FLOAT,
                packSize TEXT,
                cupPrice FLOAT,
                cupMeasure TEXT,
                servings TEXT,
                pContent FLOAT,
                PPGP FLOAT,
                PPS FLOAT
)""")
conn.commit()

#Parses JSON data and prepares it for adding to a database
#Calculates values needed for the database, including price per gram of protein
def calculations(r_dict, x):
    PPGP = 0 #Price Per Gram of Protein
    PPS = 0 #Protein Per Serve
    pContent = None #Protein content per 100 grams of product
    servings = "0" #Servings per package

    #Nutritional information string
    nutri = json.loads(r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["nutritionalinformation"])

    #These are used for products using price per EACH
    price = r_dict["Bundles"][x]["Products"][0]["Price"]
    weight = r_dict["Bundles"][x]["Products"][0]["UnitWeightInGrams"] #This weight is accurate for EA products

    #These are used for products using standard price per 100g or price per KG
    cupPrice = r_dict["Bundles"][x]["Products"][0]["CupPrice"]
    cupMeasure = r_dict["Bundles"][x]["Products"][0]["CupMeasure"]
    altWeight = r_dict["Bundles"][x]["Products"][0]["PackageSize"] #This weight is accurate for packaged products

    #Parses altWeight to be an float representing grams
    #Checks that the weight isn't variable or minimum eg. 1.4 kg - 2.4 kg
    if altWeight.find("-") == -1 and altWeight.find("min") == -1:
        if (altWeight.find("KG") != -1 or altWeight.find("kg") != -1):
            altWeight = altWeight.lower()
            if (altWeight == "per kg"):
                altWeight = 1000
            else:
                altWeight = float(re.sub('[^0-9.]','', altWeight))
                altWeight = altWeight * 1000
        elif (altWeight.find("G") != -1 or altWeight.find("g") != -1):
            altWeight = float(re.sub('[^0-9.]','', altWeight))
    else: altWeight = "n/a"


    #Attributes is an array of json objects
    #Object with id 878 contains protein per 100g info
    for i in range(len(nutri["Attributes"])):
        if (nutri["Attributes"][i]["Id"] == 878):

            pContent = nutri["Attributes"][i]["Value"]

            #Check if product contains ANY protein, skip if none
            if pContent == 0 or pContent == None or pContent == "Approx. 0" or pContent == "Approx.0" or pContent == "<0":
                print("Protein content is 0 or close to 0. Not adding")
                return None

            #Removes any non numeric or decimal characters
            pContent = re.sub('[^0-9.]','', pContent)
            #Checks if first character is a decimal, then removes it
            if (pContent.find(".") == 0):
                pContent = pContent[1:]

            try:
                pContent = float(pContent)
            except:
                print("Issue with protein content, likely multiple items")
                return None

            #Checks that pContent isn't greater than 100 (invalid protein amount)
            if (pContent >= 100):
                return None

        #ID 882 is protein per serve
        if (nutri["Attributes"][i]["Id"] == 882):
            PPS = re.sub('[^0-9.]','', nutri["Attributes"][i]["Value"])
            if (PPS.find(".") == 0):
                PPS = PPS[1:]

            try:
                PPS = float(PPS)
            except:
                print("Issue with protein serving")
                return None

        #Servings per pack total
        if (nutri["Attributes"][i]["Id"] == 544):
            servings = nutri["Attributes"][i]["Value"]
            if servings is not None:
                servings = servings.lower()
    
    #We have looped through the attributes array and protein per 100 grams is not present.
    #No need to add item
    if pContent == None:
        print("Protein per 100g IS NOT PRESENT")
        return

    #Calculates Price Per Gram of Protein
    if cupMeasure == "1KG" or cupMeasure == "1L":
        PPGP = (cupPrice / 10) / pContent
    elif cupMeasure == "100G" or cupMeasure == "100ML":
        PPGP = cupPrice / pContent
    elif cupMeasure == "10G" or cupMeasure == "10ML":
        PPGP = (cupPrice * 10) / pContent
    elif cupMeasure == "1EA" or cupMeasure == "0":
        PPGP = ((100 / weight) * price) / pContent 

    return PPGP, PPS, pContent, servings, cupPrice


#Method returns string cleaned of residual html tags
def cleanHTML(str):
    cleanr = re.compile('<.*?>')
    cleanText = re.sub(cleanr, ' ', str)
    return cleanText

#Adds data and adds item to database
def addItem(r_dict, x):

    ID = r_dict["Bundles"][x]["Products"][0]["Stockcode"] #used as ID and for URL

    try: 
        #Calculate required protein values
        PPGP, PPS, pContent, servings, cupPrice = calculations(r_dict, x)
    except:
        return

    #Check if there is a description, then clean of tags
    description = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["description"]
    if description is None:
        description = "no description"
    else:
        description = cleanHTML(description)

    print ("PPGP: " + str(PPGP) + " PPS: " + str(PPS) + " pContent: " + str(pContent) + " servings: " + str(servings))

    name = r_dict["Bundles"][x]["Name"]
    imgURL = r_dict["Bundles"][x]["Products"][0]["LargeImageFile"]
    imgURLMed = r_dict["Bundles"][x]["Products"][0]["MediumImageFile"]
    dep = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["piesdepartmentnamesjson"][1:-1]
    cat = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["piescategorynamesjson"][1:-1]
    price = r_dict["Bundles"][x]["Products"][0]["Price"]
    packSize = r_dict["Bundles"][x]["Products"][0]["PackageSize"]
    cupMeasure = r_dict["Bundles"][x]["Products"][0]["CupMeasure"]


    c.execute(""" REPLACE INTO itemDATA (ID, name, description, imgURL, imgURLMed, dep, cat, price, packSize, cupPrice, cupMeasure, servings, pContent, PPGP, PPS) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (ID, name, description, imgURL, imgURLMed, dep, cat, price, packSize, cupPrice, cupMeasure, servings, pContent, PPGP, PPS))
    conn.commit()

totalItems = 0 #Used to count total entries, even discarded ones

#Initial get request to get cookies
#Check request headers
initialHeaders = {"Host":"www.woolworths.com.au",
                    "User-Agent":"Martys Epic User Agent",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache"}

initialR = requests.get('https://www.woolworths.com.au', headers=initialHeaders)
#Cookies to be used in sending post requests
initialR_cookies = initialR.headers['Set-Cookie']
initalR_cookies_split = initialR_cookies.split(' ')

#Finding the required cookie in the string of cookies
#bm_sz is used by Akami bot manager, we need to provide it
#Or our requests will get denied
bm_sz = ""
for item in initalR_cookies_split:
    if "bm_sz" in item:
        bm_sz = item

#The ID codes used within API calls
#Using categories instead of all to eliminate non-food categories
categoryIDs = ["1-E5BEE36E","1_D5A2236","1_DEB537E","1_6E4F4E4","1_39FD49C","1_ACA2FC2","1_5AF3A0A"]

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

        headers = { "User-Agent": "Marty's Epic User Agent",
                    "Origin": "https://www.woolworths.com.au",
                    "Content-Type": "application/json",
                    "Cookie": bm_sz}

        r = requests.post('https://www.woolworths.com.au/apis/ui/browse/category', headers=headers, params=payload)

        r_dict = r.json()

        #Amount of items in the api request. Normally 36 but can be lower.
        itemCount = len(r_dict["Bundles"])

        print("Page number " + str(currentPage))

        for x in range(itemCount):
            totalItems += 1
            print(totalItems)

            print(r_dict["Bundles"][x]["Name"])
            info = r_dict["Bundles"][x]["Products"][0]["AdditionalAttributes"]["nutritionalinformation"]
            price = r_dict["Bundles"][x]["Products"][0]["Price"]

            #If Price and Nutritional info present, try to add item
            if info is not None and price is not None:
                addItem(r_dict, x)

        currentPage += 1
        #Checks if there are any more pages in the category
        morePages = False if itemCount < 36 else True
        
        #Sleep between each request to prevent getting blocked
        time.sleep(1.5)