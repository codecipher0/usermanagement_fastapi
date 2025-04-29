import httpx

API_URL = "http://localhost:8000"

# Client Functions

def create_user(name: str, email: str, contact: str):
    response = httpx.post(f"{API_URL}/users/", json={"name": name, "email": email, "contact": contact})
    if response.status_code == 200:
        print("User created:", response.json())
    else:
        print("Error creating user:", response.text)

def get_users():
    response = httpx.get(f"{API_URL}/users/")
    if response.status_code == 200:
        print("Users:", response.json())
    else:
        print("Error fetching users:", response.text)

def get_user(user_id: int):
    response = httpx.get(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        print("User:", response.json())
    else:
        print("Error fetching user:", response.text)

def update_user(user_id: int, name: str = None, email: str = None, contact: str = None):
    data = {}
    if name:
        data["name"] = name
    if email:
        data["email"] = email
    if contact:
        data["contact"] = contact

    response = httpx.put(f"{API_URL}/users/{user_id}", json=data)
    if response.status_code == 200:
        print("User updated:", response.json())
    else:
        print("Error updating user:", response.text)

def delete_user(user_id: int):
    response = httpx.delete(f"{API_URL}/users/{user_id}")
    if response.status_code == 200:
        print("User deleted")
    else:
        print("Error deleting user:", response.text)

# Example Usage
if __name__ == "__main__":
    create_user("Alice", "alice@example.com","12345")
    create_user("Bob", "bob@example.com","67890")

    get_users()

    get_user(1)

    update_user(1, name="Alice Updated")

    delete_user(2)

    get_users()