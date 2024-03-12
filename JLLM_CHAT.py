from tempmail import EMail
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
from uuid import uuid4
import json
import os

_MESSAGE: str = "Yo! How are you, fam?"

def __get_jwt__(email: str, password: str) -> str:

        """Automatically called - gets the jwt token for the user."""

        no_login_api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jbXp4dHpvbW1wbnhreW5kZGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTkwMDcwNzUsImV4cCI6MjAxNDU4MzA3NX0.YFMx-rjr69LVdy0DHSiu3Pr-WxeweQJkVOXabk4F-io"

        headers = {
            "Host": "auth.janitorai.com",
            "User-Agent": f"{UserAgent().firefox}",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=UTF-8",
            "Content-Length": "80",
            "apikey": f"{no_login_api_key}",
            "X-Client-Info": "supabase-js-web/2.39.7",
            "Origin": "https://janitorai.com",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Authorization": f"Bearer {no_login_api_key}",
            "Connection": "keep-alive",
            "TE": "trailers"
        }

        data = {
            "email": f"{email}",
            "password": f"{password}",
            "go_true_meta_security": {}
        }

        response = requests.post("https://auth.janitorai.com/auth/v1/token?grant_type=password", headers=headers, json=data)
        response.raise_for_status()

        assert response.json() is not None
        return response.json()["access_token"]

class API():

    def __init__(self, email: str, password: str) -> None:
        self.email: str = email
        self.password: str = password
        self.jwt: str = __get_jwt__(self.email, self.password)

    def generate(self, messages, max_tokens: int = 150, repetition_penalty: float = 1.2, min_p: float = 0.1, stream: bool = False, temperature: float = 0.7, stop = ["<"]):

        headers = {
            "Host": "kim.janitorai.com",
            "User-Agent": f"{UserAgent().random}",
            "Accept": "application/json, text/event-stream, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"{self.jwt}",
            "Origin": "https://janitorai.com",
            "Connection": "keep-alive",
            "Referer": "https://janitorai.com/",
            "TE": "Trailers",
            "X-Request-ID": f"{uuid4()}",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
        }

        data = {
            "max_tokens": max_tokens,
            "messages": messages,
            "repetition_penalty": repetition_penalty,
            "min_p": min_p,
            "stream": stream,
            "temperature": temperature,
            "stop": stop
        }

        print("Using JWT:", self.jwt + "\n")

        response = requests.post("https://kim.janitorai.com/generate", headers=headers, json=data, stream=stream)
        response.raise_for_status()

        if stream:

            for chunk in response.iter_lines():
                if chunk:
                    try:        delta_chunk = json.loads(chunk.decode("utf-8").removeprefix("data: "))
                    except:     pass

                    try:        yield delta_chunk["choices"][0]["delta"]["content"]
                    except:     pass

        else:

            yield response.json()["choices"][0]["message"]["content"]

def verify_mail(html_string: str) -> None:
    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')

    # Find the confirmation link
    confirmation_link = soup.select_one('.button')['href']

    # Open Selenium window and navigate to the confirmation link
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.headless = True
    driver = webdriver.Chrome(options=chrome_options)  # You can use another browser driver if needed
    driver.get("about:blank")  # Open a blank page first to prevent "data:" issue
    print(confirmation_link)
    driver.get(confirmation_link)

    print("Email verified successfully!")

    # Close the browser window
    driver.quit()

def get_email():
    email = EMail()
    return email

def get_message(email):
    msg = email.wait_for_message()
    print("Message received!")
    return msg.body

def register(email: str, password: str) -> None:
    """Automatically called - registers the user."""
    url = "https://auth.janitorai.com/auth/v1/signup?redirect_to=https://janitorai.com/profile-settings"

    token_no_login = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1jbXp4dHpvbW1wbnhreW5kZGJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE2OTkwMDcwNzUsImV4cCI6MjAxNDU4MzA3NX0.YFMx-rjr69LVdy0DHSiu3Pr-WxeweQJkVOXabk4F-io"

    headers = {
        "Host": "auth.janitorai.com",
        "User-Agent": f"{UserAgent().random}",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json;charset=UTF-8",
        "Content-Length": "146",
        "apikey": f"{token_no_login}",
        "X-Client-Info": "supabase-js-web/2.39.7",
        "Origin": "https://janitorai.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Authorization": f"Bearer {token_no_login}",
        "Connection": "keep-alive"
    }

    data = {
        "email": f"{email}",
        "password": f"{password}",
        "data": {}, 
        "gotrue_meta_security": {},
        "code_challenge": None,
        "code_challenge_method": None
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()

    # if this is printed, the user has been registered and there have been no errors
    print(f"Email {email} and password {password} Registered successfully!")

# create a new email
email = get_email()

# actually call the function to register the user
register(email=email, password="cheese123")

# wait for an email by JanitorAI
msg = get_message(email)

# verify the email
verify_mail(msg)

# create an API object. This automatically gets the JWT token for the user so we don't have to call the __get_jwt__ function
api = API(email, "cheese123")

# generate a response
for chunk in api.generate([
    {"role": "user", "content": _MESSAGE}],
    temperature=0,
    max_tokens=50,
    stream=True,
):
    print(chunk, end="", flush=True)
