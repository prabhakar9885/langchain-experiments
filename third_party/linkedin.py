import os

import requests
from dotenv import load_dotenv


def scrape_linkedin_profile(linkedin_profile_url:str, mock:bool = True):
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        response = requests.get(
            url = linkedin_profile_url,
            timeout= 30
        )
    else:
        headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}' }
        api_endpoint = 'https://nubela.co/proxycurl/api/linkedin/profile/resolve'
        params = {
            "url" : linkedin_profile_url
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=headers)
    data ={ k:v for k,v in response.json().items() if k not in ["people_also_viewed", "certificates"] and v not in ([],"","",None) }
    if data.get('groups'):
        for group in data.get('groups'):
            group.pop('profile_pic_url')
    return data

if __name__ == '__main__':
    load_dotenv()
    response = scrape_linkedin_profile("")
    print(response)