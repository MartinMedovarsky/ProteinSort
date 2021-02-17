import requests
import time
import csv

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
def calcParse(r_dict, x):
    return True

#Adds data and adds item to database
def addItem(r_dict, x):

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
            if info is None or info.find("Protein") == -1:
                print("No protein")
            else:
                print("Protein!")
                addItem(r_dict, x)



        currentPage += 1
        morePages = pageCheck(itemCount) 
        time.sleep(3)
    