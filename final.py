import requests
import json 
import unittest
import pickle
from yelp.client import Client
from yelp.oauth1_authenticator import Oauth1Authenticator

from pprint import pprint

def pretty(obj):
	return json.dumps(obj, sort_keys=True, indent=2)

CACHE_FNAME = 'cache.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def getWithCaching(baseurl, url_params):
    BASE_URL = baseurl
    p_diction = url_params
    full_url = requestURL(BASE_URL, p_diction)

    if full_url in CACHE_DICTION:
        print('using cache')
        # use stored response
        response_text = CACHE_DICTION[full_url]
    else:
        print('fetching')
        # do the work of calling the API
        response = requests.get(full_url)
        # store the response
        CACHE_DICTION[full_url] = response.text
        response_text = response.text

        cache_file = open(CACHE_FNAME, 'w')
        cache_file.write(json.dumps(CACHE_DICTION))
        cache_file.close()

    return response_text

def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res

def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url


##ACCESSING THE YELP API!##
oauth_consumer_key = "TMpOtbBU49_Uo3oTkH25vA"
oauth_signature_method = "hmac-sha1"
consumer_secret = "uIek73K0HMbFkBC_di30JkNXrvQ"
oauth_token = "G52KrZ7q6NPZdBMCjnBkiZD71-o22fE5"
oauth_signature	 = "11vwoapu7AnYqVRVQ6IqT-_HaL0"

auth = Oauth1Authenticator(
    consumer_key=oauth_consumer_key,
    consumer_secret=consumer_secret,
    token=oauth_token,
    token_secret=oauth_signature
)

client = Client(auth)

params =  {
    'term': 'food',
    'limit': 40,
}
response = client.search("Ann Arbor", **params)

yelp_data= {}
for each in response.businesses:
	yelp_data[each.name] = each.rating

# print pretty(yelp_data)



	
### Accessing the Facebook API#########

access_token = "EAAXPPlAm9IYBANklbFpUmALFW7S7oii4HhRSZBKmZBU8UyN88vmvdzW7nbl63bXjnwbV2ZA532FuIhvBZAJGdXhjjf9E2E7eCM7bd43fEFs3YNxoWqmECQ3LiJmB8uY0WDantWQTXBd46IvG88vrFYzZCfCZBvBDoXKNFZBTOd5RAZDZD

url_params= {}
baseurl= "https://graph.facebook.com/v2.7/search"
url_params["access_token"]= access_token
url_params["q"]= "ann+arbor+restaurants"
url_params["type"]= "page"
url_params["limit"]= 100

d= getWithCaching(baseurl, url_params)
# d= requests.get(baseurl, params= url_params)
data= json.loads(d)
# print data["data"][0]["name"]

data_list= []
for each in data["data"]:
	data_list.append(each)
#print data_list


class FacebookRestaurant():
	def __init__(self, each= {}):
		#for each in lst:
		self.name= each["name"]
		self.id= each["id"]

		access_token2 = "EAACEdEose0cBABaZCZBW7WZCjGC32xMZBKQL0pqW2sGquwEAYgLZCwzKpP5VoiD3mSXJWi1ei0WWKfEZBuCQs9zS7hFZBQ7Ill83gPEbTZCUbYTLm7La2PPn8mCGWfOS7Te8PYZAExxhiddkAuMnekxCRGdiU629dGJOloJRrq7MnXgZDZD"
		url_params2= {}
		baseurl2= "https://graph.facebook.com/v2.7/"
		url_params2["access_token"]= access_token2
		url_params2["fields"]= "overall_star_rating"
		baseurl3= baseurl2+ str(self.id)

		f= getWithCaching(baseurl3, url_params2)
		rdata= json.loads(f)
		self.rating= rdata["overall_star_rating"]

	def get_rating(self):
		return self.rating
	

	def get_yelp_data(self): #get data from my yelp dictionary and compare it 
		self.yelp_rating= ""
		#print yelp_data.keys()
		for key in yelp_data.keys():
			# print key, self.name
			if self.name in key: #find out a way to compare ratings
				self.yelp_rating = yelp_data[key]
				break
			elif key in self.name:
				self.yelp_rating= yelp_data[key]
				break
			else:
				self.yelp_rating= "No rating on Yelp."

		return self.yelp_rating

	def __str__(self): #finish this
		 return "Name: {}\nFacebook rating: {}\nYelp Rating: {}\n".format(self.name,self.rating, self.yelp_rating) #want to add yelp rating into here as well

#print data_list
inst_list= []
for each in data_list:
	y= FacebookRestaurant(each)
	y.get_yelp_data()
	inst_list.append(y)
	# print y
# print inst_list

def get_sorted(lst):
	sorted_list= sorted(inst_list, key= lambda x: x.rating, reverse= True)
	return sorted_list

x= get_sorted(inst_list)

for instance in x:
	print(instance)
	

def cache_yelp(cache_fname):
    params= {}
    params['term'] = 'food'
    params['limit']= 40


    oauth_consumer_key = "TMpOtbBU49_Uo3oTkH25vA"
    oauth_signature_method = "hmac-sha1"
    consumer_secret = "uIek73K0HMbFkBC_di30JkNXrvQ"
    oauth_token = "G52KrZ7q6NPZdBMCjnBkiZD71-o22fE5"
    oauth_signature	 = "11vwoapu7AnYqVRVQ6IqT-_HaL0"

   
    auth = Oauth1Authenticator(
    consumer_key = oauth_consumer_key,
    consumer_secret = consumer_secret,
    token = oauth_token,
    token_secret = oauth_signature
    )    
     
    client = Client(auth)

    try:
        fobj = open(cache_fname, 'rb')
        cache_saved = pickle.load(fobj)
        fobj.close()
    except:
        feedback = client.search("Ann Arbor", **params)
        print(feedback)

        yelp_responses = {}
        for each in feedback.businesses:
            yelp_responses[each.name] = each.rating
        cache_saved = yelp_responses
        yelp_cache = open(cache_fname, 'wb')
        pickle.dump(cache_saved, yelp_cache)
   
    parsed_response = cache_saved
    return parsed_response
    

cache_yelp("yelp_cache.txt")

### TESTING CODE ###

class Values(unittest.TestCase):
    def test_fb_cache_1(self):
    	self.assertEqual(type(data), type({}), "testing type of first Facebook data call from cache file.")
    def test_instance1(self):
    	self.assertEqual(type(y.name), type(u""), "testing type of restaurant name in __init__")
    def test_instance_list(self):
    	self.assertEqual(type(inst_list), type([]), "testing type of instance inst_list")
    def test_rating(self):
    	self.assertEqual(len(x), 29, "testing length of my sorted list that was returned by my get_sorted function.")
    def test_data_list(self):
    	self.assertEqual(type(data["data"]), type([]), "testing type of data")
    def test_yelp_data(self):
    	self.assertEqual(type(yelp_data), type({}), "testing the type of yelp data to be used in class method")




unittest.main(verbosity=2)
