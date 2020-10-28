import json

def getUsers(fileName):
    file = open(fileName, "r")
    data = json.loads(file.read())
    logins = []
    for idx in data:
        logins.append(idx["login"])

    return logins

def getCompany(user):
    file = open("data/UserCompany.json", "r")
    data = json.loads(file.read())
    print(data[user])
    # for idx in data:
    #     print(idx[user])
    #     break     

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
    

# def main():
#     file_name = "data/flutter_contributors.json"
#     logins = getUsers(file_name)
#     user = "caitp"
#     getCompany(user)
    
# main()
