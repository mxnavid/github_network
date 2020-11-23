import json


""" 
    This function returns list of user for a given file.
    Input: File Name (str)
    Return : List of users in str (list)
"""
def getUsers(fileName):
    file = open(fileName, "r")
    data = json.loads(file.read())
    logins = []
    for idx in data:
        logins.append(idx)

    return logins


"""
    This fucntion returns the name of the company the user is associated with. 
    Input: UserName (str)
    Return: Comany Name (str)
"""
def getCompany(user):
    file = open("data/UserCompany.json", "r")
    data = json.loads(file.read())
    username = data[user]
    if username == None:
        return "Unknown Company"
    if "@" in username:
        username = username.replace("@","")
    username = username.lower()
    return username


"""
    This function returns the path of the file with repo name
    Input: Repo Name (str)
    Output: Path of the repo (str)
"""

def finder_file(repo_name):
    if repo_name == "Fluter":
        return "data/flutter_contributors.json"
    elif repo_name == "VSCode":
        return "data/vscode_contributors.json"
    elif repo_name == "Kubernetes":
        return "data/kubernetes_contributors.json"
    elif repo_name == "React":
        return "data/react_contributors.json"
    elif repo_name == "TypeScript":
        return "data/typescript_contributors.json"
    elif repo_name == "Flow":
        return "data/flow_contributors.json"
    return "Not Found"
    


