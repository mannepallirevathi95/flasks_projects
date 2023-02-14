import requests
def user_section():
    response = requests.request(method = "get",url = "https://randomuser.me/api").json()
    user_data = {}
    user_data["gender"] = response['results'][0]['gender']
    user_data["first_name"] = response['results'][0]['name']['first']
    user_data["last_name"] = response['results'][0]['name']['last']
    user_data["state"] = response['results'][0]['location']['state']
    user_data["country"] = response['results'][0]['location']['country']
    user_data["email"] = response['results'][0]['email']
    user_data["user_name"] = response['results'][0]['login']['username']
    user_data["password"] = response['results'][0]['login']['password']
    user_data["age"] = response['results'][0]['dob']['age']
    user_data["cell"] = response['results'][0]['cell']

    print("user generated!")

    return user_data

print(user_section())