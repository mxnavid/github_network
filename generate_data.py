import json
import glob
import requests

listOfFiles = (glob.glob("data/*_contributors.json"))

mapOfUserObjects = {}
mapOfUserCompany = {}
mapOfUserOrg = {}

# Add Github Token here
# token = "#"

for file in listOfFiles:
    with open(file) as f:
        data = json.load(f)
        for object in data:
            # Set the username as login from the json files
            username = str(object)
            url = 'https://api.github.com/users/{0}'.format(username)
            r = requests.get(url)# , headers={'Authorization': 'Bearer {}'.format(token)})
            response = r.json()
            mapOfUserObjects[username] = r.json()
            if 'company' in response:
                mapOfUserCompany[username] = response['company']
            else: 
                mapOfUserCompany[username] = None
            
            # Create another get request to get the organization data. This is commented out to prevent rate limits
            # orgs = requests.get('https://api.github.com/users/{0}/orgs'.format(username), headers={'Authorization': 'Bearer {}'.format(token)})
            # mapOfUserOrg[username] = orgs.json()





# # Dump the maps into json files
with open("data/UserObjects.json", "w") as outfile:
    json.dump(mapOfUserObjects, outfile)

with open("data/UserCompany.json", "w") as outfile:
    json.dump(mapOfUserCompany, outfile)

# with open("UserOrg.json", "w") as outfile:
#     json.dump(mapOfUserOrg, outfile)

# This is for going through the pages
# mapOfUsers = {}

# for x in range(1,6):
#     r = requests.get('https://api.github.com/repos/kubernetes/kubernetes/contributors?per_page=100&page={}'.format(x) ,headers={'Authorization': 'Bearer {}'.format(token)})
#     response = r.json()
#     for object in response:
#         mapOfUsers[str(object['login'])] = object

# print(len(mapOfUsers))
# with open("data/kubernetes_contributors.json", "w") as outfile:
#     json.dump(mapOfUsers, outfile)


