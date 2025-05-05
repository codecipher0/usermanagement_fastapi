import httpx

API_URL = "http://localhost:8000"

# Client Functions

def login(email: str, password: str) -> str:
    response = httpx.post(f"{API_URL}/token", data={"username": email, "password": password})
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("Login successful.")
        return token
    else:
        raise Exception(f"Login failed: {response.text}")

def create_user(name: str, email: str, contact: str, password: str):
    response = httpx.post(f"{API_URL}/users/", json={"name": name, "email": email, "contact": contact, "password": password})
    if response.status_code == 200:
        print("User created:", response.json())
    else:
        print("Error creating user:", response.text)

def get_users(token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(f"{API_URL}/users/", headers=headers)
    if response.status_code == 200:
        print("Users:", response.json())
    else:
        print("Error fetching users:", response.text)

def get_user(user_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(f"{API_URL}/users/{user_id}", headers=headers)
    if response.status_code == 200:
        print("User:", response.json())
    else:
        print("Error fetching user:", response.text)

def update_user(user_id: int, token: str, name: str = None, email: str = None, contact: str = None):
    data = {}
    if name:
        data["name"] = name
    if email:
        data["email"] = email
    if contact:
        data["contact"] = contact

    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.put(f"{API_URL}/users/{user_id}", json=data, headers=headers)
    if response.status_code == 200:
        print("User updated:", response.json())
    else:
        print("Error updating user:", response.text)

def delete_user(user_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.delete(f"{API_URL}/users/{user_id}", headers=headers)
    if response.status_code == 200:
        print("User deleted")
    else:
        print("Error deleting user:", response.text)
        
def add_comment(comment: str, token:str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(f"{API_URL}/comments/", json={"comment": comment}, headers=headers)
    if response.status_code == 200:
        print("Comment added:", response.json())
    else:
        print("Error adding comment:", response.text)
        
def get_comments(token: str, skip: int=0, limit: int = 5):
    headers = {"Authorization": f"Bearer {token}"}
    #response = httpx.get(f"{API_URL}/comment/", headers=headers)
    response = httpx.get(f"{API_URL}/comments/?skip={skip}&limit={limit}")
    if response.status_code == 200:
        print("Comments:", response.json())
    else:
        print("Error fetching comments:", response.text)
        
def add_reply(reply: str, parent_id: int, token:str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.post(f"{API_URL}/comments/", json={"comment": reply, "parent_id": parent_id}, headers=headers)
    if response.status_code == 200:
        print("Comment added:", response.json())
    else:
        print("Error adding comment:", response.text)
        
def get_comment(token: str, comment_id: int):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(f"{API_URL}/comments/{comment_id}", headers=headers)
    if response.status_code == 200:
        print("Comments:", response.json())
    else:
        print("Error fetching comments:", response.text)
        
def delete_comment(comment_id: int, token: str):
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.delete(f"{API_URL}/comments/{comment_id}", headers=headers)
    if response.status_code == 200:
        print("Comment deleted")
    else:
        print("Error deleting comment:", response.text)

# Example Usage
if __name__ == "__main__":
    #uncomment to create initial user
    #create_user("Jay", "Jay@example.com","12345","pass1234")
    #token = login("Jay@example.com", "pass1234")
    #create_user("Jas", "Jas@example.com","67890","pass6789")
    token = login("Jas@example.com", "pass6789")
    #create_user("Bob", "bob@example.com","67890", token)

    get_users(token)
    
    #add_comment("Hello!", token)
    #add_comment("How are you!", token)
    #add_comment("Konnichiwa!", token)
    #add_comment("Ohayou!", token)
    #add_comment("Kamusta!", token)
    
    #add_comment("comment6!", token)
    #add_comment("comment7!", token)
    #add_comment("comment8!", token)
    #add_comment("comment9!", token)
    #add_comment("comment10!", token)
    
    #add_comment("comment11!", token)
    #add_comment("comment12!", token)
    #add_comment("comment13!", token)
    #add_comment("comment14!", token)
    #add_comment("comment15!", token)
    
    #add_reply("reply1", 1, token)
    #add_reply("reply2", 3, token)
    #add_reply("reply3", 3, token)
    #token = login("Jas@example.com", "pass6789")
    #add_reply("reply4", 3, token)
    
    #get_comments(token)
    #get_comment(token,1)
    
    get_comments(token)
    #delete_comment(9, token)
    print("-----------")
    get_comment(token, 3)
    
    #add_reply("Wazup!",1,token)
    #add_reply("Afternoon!",1,token)
    
    #get_comment(1, token)

    #get_user(1, token)

    #update_user(1,token, name="jay")

    #delete_user(2, token)

    #get_users(token)
    
    