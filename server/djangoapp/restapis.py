import requests
import json
import os
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from decouple import config
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


print(config('WATSON_NLU_API_KEY'))


# Inside your get_request function
def get_request(url, **kwargs):
   try:
       response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
       response.raise_for_status()  # Raise an HTTPError for bad status codes
       json_data = response.json()
   except requests.exceptions.RequestException as e:
       # If any error occurs during the request
       print("Network exception occurred:", str(e))
       return None


   status_code = response.status_code
   if status_code == 500:
       print("Server Error: Internal Server Error")
       return None


   print("With status {} ".format(status_code))
   return json_data






def post_request(url, json_payload, **kwargs):
   print("Payload: ", json_payload, ". Params: ", kwargs)
   print(f"POST {url}")
   try:
       response = requests.post(url, headers={'Content-Type': 'application/json'},
                                json=json_payload, params=kwargs)
   except:
       # If any error occurs
       print("Network exception occurred")
   status_code = response.status_code
   print("With status {} ".format(status_code))
   json_data = json.loads(response.text)
   return json_data




def get_dealers_from_cf(url, **kwargs):
   results = []
   # Call get_request with a URL parameter
   json_result = get_request(url)
   if json_result:
       # Get the row list in JSON as dealers
       dealers = json_result
       # For each dealer object
       for dealer_doc in dealers:
           # Create a CarDealer object with values in `doc` object
           dealer_obj = CarDealer(
               address=dealer_doc["address"],
               city=dealer_doc["city"],
               full_name=dealer_doc["full_name"],
               id=dealer_doc["id"],
               lat=dealer_doc["lat"],
               long=dealer_doc["long"],
               short_name=dealer_doc["short_name"],
               st=dealer_doc["st"],
               zip=dealer_doc["zip"]
           )
           results.append(dealer_obj)
   return
  
def get_dealer_by_id(url, dealer_id):
   # Call get_request with the dealer_id param
   json_result = get_request(url, dealer_id=dealer_id)


   if json_result and isinstance(json_result, list) and len(json_result) > 0:
       dealer = json_result[0]  # Get the first element of the list
       dealer_obj = CarDealer(
           address=dealer.get("address", ""),
           city=dealer.get("city", ""),
           full_name=dealer.get("full_name", ""),
           lat=dealer.get("lat", ""),
           long=dealer.get("long", ""),
           short_name=dealer.get("short_name", ""),
           st=dealer.get("st", ""),
           zip=dealer.get("zip", ""),
           id=dealer["id"],
       )


       return dealer_obj
   else:
       # Handle the case where json_result is None, empty, or not a list
       return None




def get_dealer_reviews_from_cf(url, dealer_id):
   results = []
   # Perform a GET request with the specified dealer id
   json_result = get_request(url)


   if json_result:
       # Get all review data from the response
       reviews = json_result
       # For every review in the response
       for review in reviews:
           # Create a DealerReview object from the data
           # These values must be present
           review_content = review["review"]
           review_id = review["_id"]
           name = review["name"]
           purchase = review["purchase"]
           dealership = review["dealership"]


           # Initialize sentiment with a default value
           sentiment = "neutral"


           try:
               # These values may be missing
               car_make = review["car_make"]
               car_model = review["car_model"]
               car_year = review["car_year"]
               purchase_date = review["purchase_date"]


               # Creating a review object with sentiment
               review_obj = DealerReview(
                   dealership=dealership, id=review_id, name=name,
                   purchase=purchase, review=review_content, car_make=car_make,
                   car_model=car_model, car_year=car_year, purchase_date=purchase_date,
                   sentiment=sentiment
               )
           except KeyError:
               print("Something is missing from this review. Using default values.")
               # Creating a review object with some default values
               review_obj = DealerReview(
                   dealership=dealership, id=review_id, name=name, purchase=purchase,
                   review=review_content, sentiment=sentiment
               )


           # Analysing the sentiment of the review object's review text and saving it to the object attribute "sentiment"
           review_obj.sentiment = analyze_review_sentiments(review_obj.review)
           print(f"sentiment: {review_obj.sentiment}")


           # Saving the review object to the list of results
           results.append(review_obj)


   return results


# Calls the Watson NLU API and analyses the sentiment of a review
def analyze_review_sentiments(review_text):
   # Watson NLU configuration
   try:
       if os.environ['env_type'] == 'PRODUCTION':
           url = os.environ['WATSON_NLU_URL']
           api_key = os.environ["WATSON_NLU_API_KEY"]
   except KeyError:
       url = config('WATSON_NLU_URL')
       api_key = config('WATSON_NLU_API_KEY')


   version = '2021-08-01'
   authenticator = IAMAuthenticator(api_key)
   nlu = NaturalLanguageUnderstandingV1(
       version=version, authenticator=authenticator)
   nlu.set_service_url(url)


   # get sentiment of the review
   try:
       response = nlu.analyze(text=review_text, features=Features(
           sentiment=SentimentOptions())).get_result()
       print(json.dumps(response))
       # sentiment_score = str(response["sentiment"]["document"]["score"])
       sentiment_label = response["sentiment"]["document"]["label"]
   except:
       print("Review is too short for sentiment analysis. Assigning default sentiment value 'neutral' instead")
       sentiment_label = "neutral"


   # print(sentiment_score)
   print(sentiment_label)


   return sentiment_label
