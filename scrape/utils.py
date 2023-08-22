from abc import ABC, abstractmethod
import requests
import json
import os


class SearchCriteria():

    def __init__(self, job_title, job_location, adzuna_location = None):
        self.job_title = job_title
        self.job_location = job_location
        self.adzuna_location = findCountry(self.job_location)

    


class HttpClient(ABC):
    

    

    def __init__(self, url, payload = None, headers = None, location = None):
        self.url = url
        self.payload = payload
        self.headers = headers
        self.location = location
        self.initialize()

    @abstractmethod
    def initialize(self):
        pass




    def sendRequest(self):

        url = self.url
        payload = self.payload
        headers = self.headers

        successful = False

        while not successful:
            try:
                
                response = requests.request("POST", url, headers=headers, data=payload).text




                self.response = response

                successful = True



            except requests.exceptions.RequestException as e:
                pass

        return self.response


    def jsonParse(self):

        try:
            parsed_data = json.loads(self.response)
            return parsed_data
        except AttributeError as ae:
            raise Exception("No response data found to parse.")
        except json.JSONDecodeError as jde:
            return "API Limit exceeded."


    


def findCountry(location_name):

    name = location_name



    if name == "usa" or name == "USA" or name == "america" or name == "America" or name == "AMERICA":
        return "us"



    country_full_url = 'https://restcountries.com/v3.1/name/{}?fullText=true'.format(name)

    country_code = 'https://restcountries.com/v3.1/alpha/{}'.format(name)

    api_url = 'https://api.api-ninjas.com/v1/city?name={}'.format(name)


    response = requests.get(country_full_url)



    if response.status_code == 404 or response.status_code == 400:
        response = requests.get(country_code)


        if response.status_code == 404 or response.status_code == 400:
            response = requests.get(api_url,  headers={'X-Api-Key': '0A6zy36olH/z2sLljLpFTA==IKCunK68Pdg5pfvD'} )


            try:
                country = json.loads(response.content)[0]['country'].lower()
            except IndexError:
                return None
            

            return country
            
        else:

            return name



    elif response.status_code == 200:

        return json.loads(response.content)[0]['cca2'].lower()

    
def getApiKeys():
    
    adzuna_app_id = os.environ.get('adzuna_app_id')
    adzuna_app_key = os.environ.get('adzuna_app_key')
    jooble_api_key = os.environ.get('jooble_api_key')

    return adzuna_app_id, adzuna_app_key, jooble_api_key

