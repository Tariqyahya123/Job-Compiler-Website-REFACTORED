from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
import json
import random
from .models import ResultJobs
from .utils import SearchCriteria, HttpClient, findCountry, getApiKeys, urlEncodeJobTitleForAdzuna

  





class JoobleResults(HttpClient):

    def initialize(self):
        self.list = self.mapResultsToModelAndReturnList()

    
    def mapResultsToModelAndReturnList(self):

        self.sendRequest()



        parsed_data = self.jsonParse()

        if parsed_data == "API Limit exceeded.":
            return None


        my_jooble_results = []


        for i in parsed_data['jobs']:
            try:
                my_jooble_results.append(ResultJobs(job_id=i['id'] , title=i['title'], company=i['company'], location=i['location'], link=i['link']))
            except KeyError:
                my_jooble_results.append(ResultJobs(job_id=i['id'] , title=i['title'], location=i['location'], link=i['link']))


        return my_jooble_results


class AdzunaResults(HttpClient):

    def initialize(self):
        self.list = self.mapResultsToModelAndReturnList()



    
    def mapResultsToModelAndReturnList(self):

      
        self.sendRequest()
        
        parsed_data = self.jsonParse()

            

        my_adzuna_results = []


        for i in parsed_data['results']:


            temp = ""

            location = ""

            for j in range(0, (len(i['location']['area']) - 1)):

                if j == 0:

                    temp = i['location']['area'][j]
                    
                else:

                    temp = i['location']['area'][j] + ", " + temp

                location = temp



            my_adzuna_results.append(ResultJobs(job_id=i['id'], title=i['title'], location=location, link=i['redirect_url']))


        return my_adzuna_results



def returnHome(request):

    if request.method == "POST":

        return renderResults(request)
        
    else:

        return render(request, 'scrape/scrape.html')



    
def mapUserEntryToObject(request):
    search_criteria = SearchCriteria(job_title=request.POST['job_name'], job_location=request.POST['location_name'])

    return search_criteria




def getResults(object):


    adzuna_app_id, adzuna_app_key, jooble_api_key = getApiKeys()



    

    jooble_payload = {
        "keywords": object.job_title,
        "location": object.job_location
    }

    jooble_results = JoobleResults(url=f"https://jooble.org/api/{jooble_api_key}", 
            payload=json.dumps(jooble_payload),  headers={'Content-Type': 'text/plain'})


    adzuna_country_list = ['gb', 'us', 'at', 'au', 'be', 'br', 'ca', 'ch', 'de', 'es', 'fr', 'in', 'it', 'mx', 'nl', 'nz', 'pl', 'ru', 'sg', 'za']

    if object.adzuna_location in adzuna_country_list:


        adzuna_job_title = urlEncodeJobTitleForAdzuna(object.job_title)



        adzuna_results = AdzunaResults(url=f'http://api.adzuna.com/v1/api/jobs/{object.adzuna_location}/search/1?app_id={adzuna_app_id}&app_key={adzuna_app_key}&results_per_page=20&what={adzuna_job_title}&content-type=application/json')

        try:

            combined_list =  adzuna_results.list + jooble_results.list

        except TypeError as te:


            if 'can only concatenate list (not "NoneType") to list' in str(te):

                return adzuna_results.list

            else:

                raise ValueError("An unexpected TypeError occurred:", te)


        random.shuffle(combined_list)

        return combined_list

    else:

        if jooble_results.list == None and object.adzuna_location == "" :


            adzuna_job_title = urlEncodeJobTitleForAdzuna(object.job_title)


            all_regions_list = []

            for i in adzuna_country_list[:2]:

                adzuna_results = AdzunaResults(url=f'http://api.adzuna.com/v1/api/jobs/{i}/search/1?app_id={adzuna_app_id}&app_key={adzuna_app_key}&results_per_page=20&what={adzuna_job_title}&content-type=application/json')

                all_regions_list = all_regions_list + adzuna_results.list
                

            return all_regions_list


        elif object.adzuna_location == "":

            adzuna_job_title = urlEncodeJobTitleForAdzuna(object.job_title)


            all_regions_list = []

            for i in adzuna_country_list[:2]:

                adzuna_results = AdzunaResults(url=f'http://api.adzuna.com/v1/api/jobs/{i}/search/1?app_id={adzuna_app_id}&app_key={adzuna_app_key}&results_per_page=20&what={adzuna_job_title}&content-type=application/json')

                all_regions_list = all_regions_list + adzuna_results.list

            combined_list =  all_regions_list + jooble_results.list

            random.shuffle(combined_list)


            return combined_list





        return jooble_results.list



def renderResults(request):

    search_criteria_object = mapUserEntryToObject(request)



    results = getResults(search_criteria_object)


    if len(results) == 0:
        return render(request, 'scrape/results-none.html')






    return render(request, 'scrape/results.html', {'jobs' : results})






def renderStarred(request):
    return render(request, 'scrape/starred.html')
   

    
    
