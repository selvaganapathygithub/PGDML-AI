from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from rasa_core.events import Restarted
from collections import OrderedDict
import zomatopy
import json
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd

class ActionValidateLocation(Action):
	def name(self):
		return 'action_validate_location'
		
	def run(self, dispatcher, tracker, domain):
		list_loc = ["ahmedabad", "bangalore", "chennai", "delhi", "hyderabad", "kolkata", "mumbai", "pune", "agra", "ajmer", "aligarh", "amravati", "amritsar", "asansol", "aurangabad", "bareilly", "belgaum", "bhavnagar", "bhiwandi", "bhopal", "bhubaneswar", "bikaner", "bokaro steel city", "chandigarh", "coimbatore", "cuttack", "dehradun", "dhanbad", "durg-bhilai nagar", "durgapur", "erode", "faridabad", "firozabad", "ghaziabad", "gorakhpur", "gulbarga", "guntur", "gurgaon", "guwahati‚ gwalior", "hubli-dharwad", "indore", "jabalpur", "jaipur", "jalandhar", "jammu", "jamnagar", "jamshedpur", "jhansi", "jodhpur", "kannur", "kanpur", "kakinada", "kochi", "kottayam", "kolhapur", "kollam", "kota", "kozhikode", "kurnool", "lucknow", "ludhiana", "madurai", "malappuram", "mathura", "goa", "mangalore", "meerut", "moradabad", "mysore", "nagpur", "nanded", "nashik", "nellore", "noida", "palakkad", "patna", "pondicherry", "prayagraj", "raipur", "rajkot", "rajahmundry", "ranchi", "rourkela", "salem", "sangli", "siliguri", "solapur", "srinagar", "sultanpur", "surat", "thiruvananthapuram", "thrissur", "tiruchirappalli", "tirunelveli", "tiruppur", "ujjain", "bijapur", "vadodara", "varanasi", "vasai-virar city", "vijayawada", "visakhapatnam", "warangal"]
		loc = tracker.get_slot('location')
		#dispatcher.utter_message(loc)
		if loc is not None:
			if loc.lower() in list_loc:
				return[SlotSet('location',loc)]
			else:
				dispatcher.utter_message("Sorry we do not operate in this area yet. try some other location")
				return[SlotSet('location',None)]
		else:
			dispatcher.utter_message("Sorry I could not understand the location you provided. try some other location")
			return[SlotSet('location', None)]

class ActionValidateCuisine(Action):
	def name(self):
		return 'action_validate_cuisine'
	
	def run(self, dispatcher, tracker, domain):
		list_cuisine = ["chinese","mexican","american","italian","south indian","north indian"]
		cuisine = tracker.get_slot('cuisine')
		if cuisine is not None:
			if cuisine.lower() in list_cuisine:
				#dispatcher.utter_message(cuisine)
				return[SlotSet('cuisine',cuisine)]
			else:
				dispatcher.utter_message("Sorry this is not a valid cuisine. please check for typing errors")
				return[SlotSet('cuisine',None)]
		else:
			dispatcher.utter_message("Sorry I could not understand the cuisine name you provided")
			return[SlotSet('cuisine', None)]			
	
class ActionValidateBudget(Action):
	def name(self):
		return 'action_validate_budget'
	
	def run(self, dispatcher, tracker, domain):
		cost_queried = tracker.get_slot('budget')
		cost_queried = cost_queried.lower()
		#dispatcher.utter_message(cost_queried) 
		if cost_queried == 'lesser than rs 300' or cost_queried == '<300' or cost_queried == 'less than 300':
			return[SlotSet('budget', 'low')]
		elif cost_queried == 'rs 300 to 700' or cost_queried == '300-700 range' or cost_queried == 'between 300 and 700':
			return[SlotSet('budget', 'mid')]
		elif cost_queried == 'more than 700' or cost_queried == '>700' or cost_queried == 'greater than 700':
			return[SlotSet('budget', 'high')]
		else:
			return[SlotSet('budget', '')]
				
class ActionSearchRestaurants(Action):
	def name(self):
		return 'action_restaurant'
		
	def run(self, dispatcher, tracker, domain):
		response=""
		config={ "user_key":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"} 
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		if budget == 'low':
			budget_min = 0
			budget_max = 300
		elif budget == 'mid':
			budget_min = 301
			budget_max = 700
		elif budget == 'high':
			budget_min = 701
			budget_max = 20000
		
		cols = ['restaurant name', 'restaurant address', 'avg. budget for two', 'zomato rating']
		resrnt_df = pd.DataFrame(columns = cols)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'american':1,'chinese':25,'mexican':73,'italian':55,'north indian':50,'south indian':85}
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 20)
		d = json.loads(results)
		
#		dispatcher.utter_message(str(resrnt_df['restaurant name'].count()))
		
		if d['results_found'] != 0:
			for restaurant in d['restaurants']:
				curr_res = {'zomato rating':restaurant['restaurant']["user_rating"]["aggregate_rating"],'restaurant name':restaurant['restaurant']['name'],'restaurant address': restaurant['restaurant']['location']['address'], 'avg. budget for two': restaurant['restaurant']['average_cost_for_two']}		
				if (curr_res['avg. budget for two'] >= budget_min) and (curr_res['avg. budget for two'] <= budget_max):						
					resrnt_df.loc[len(resrnt_df)] = curr_res
		
		# sort restarants on rating  
		resrnt_df = resrnt_df.sort_values(['zomato rating','avg. budget for two'], ascending=[False,True])
		resrnt_df10 = resrnt_df.head(10)
		resrnt_df = resrnt_df.head(5)
		resrnt_df = resrnt_df.reset_index(drop=True)
		resrnt_df.index = resrnt_df.index.map(str)
		
		# Display only top 5 records
		if len(resrnt_df) != 0:
			for index, row in resrnt_df.iterrows():
				response = response+ index + ". Found \""+ row['restaurant name']+ "\" in "+ row['restaurant address']+" has been rated "+ row['zomato rating']+"\n"
		else:
			response = 'Found 0 restaurants in given price range'
			
		dispatcher.utter_message(response)
		return [SlotSet('budget',budget)]



class ActionValidateEmail(Action):
	def name(self):
		return 'action_validate_email'
		
	def run(self, dispatcher, tracker, domain):
		
		regex = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'
		email_check = tracker.get_slot('email')
		#dispatcher.utter_message(email_check) 
		if email_check is not None:
			if re.search(regex, email_check):
				#dispatcher.utter_message(email_check) 
				return[SlotSet('email',email_check)]
			else:
				dispatcher.utter_message("Sorry this is not a valid email. please check for typing errors")
				return[SlotSet('email',None)]
		else:
			dispatcher.utter_message("Sorry I could not understand the email address which you provided? Please provide again")
			return[SlotSet('email', None)]			
	

class ActionSendEmail(Action):
	def name(self):
		return 'action_email'		
    		
	def run(self, dispatcher, tracker, domain):
		config={ "user_key":"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"} 
		zomato = zomatopy.initialize_app(config)
		loc = tracker.get_slot('location')
		cuisine = tracker.get_slot('cuisine')
		budget = tracker.get_slot('budget')
		if budget == 'low':
			budget_min = 0
			budget_max = 300
		elif budget == 'mid':
			budget_min = 301
			budget_max = 700
		elif budget == 'high':
			budget_min = 701
			budget_max = 20000
		
		cols = ['restaurant name', 'restaurant address', 'avg. budget for two', 'zomato rating']
		resrnt_df = pd.DataFrame(columns = cols)
		location_detail=zomato.get_location(loc, 1)
		d1 = json.loads(location_detail)
		lat=d1["location_suggestions"][0]["latitude"]
		lon=d1["location_suggestions"][0]["longitude"]
		cuisines_dict={'american':1,'chinese':25,'mexican':73,'italian':55,'north indian':50,'south indian':85}
		results=zomato.restaurant_search("", lat, lon, str(cuisines_dict.get(cuisine)), 20)
		d = json.loads(results)
		
#		dispatcher.utter_message(str(resrnt_df['restaurant name'].count()))
		
		d = json.loads(results)
		
#		dispatcher.utter_message(str(resrnt_df['restaurant name'].count()))
		
		if d['results_found'] != 0:
			for restaurant in d['restaurants']:
				curr_res = {'zomato rating':restaurant['restaurant']["user_rating"]["aggregate_rating"],'restaurant name':restaurant['restaurant']['name'],'restaurant address': restaurant['restaurant']['location']['address'], 'avg. budget for two': restaurant['restaurant']['average_cost_for_two']}		
				if (curr_res['avg. budget for two'] >= budget_min) and (curr_res['avg. budget for two'] <= budget_max):						
					resrnt_df.loc[len(resrnt_df)] = curr_res
		
		# sort restarants on rating  
		resrnt_df = resrnt_df.sort_values(['zomato rating','avg. budget for two'], ascending=[False,True])
		
		email = tracker.get_slot('email')
		gmail_user = 'selvaupgrad@gmail.com' 
		gmail_password = 'xxxxxxxxxxx' 
		sent_from = gmail_user  
		to = str(email)
		msg = MIMEMultipart('alternative')
		msg['Subject'] = "Restaurant Details"
		msg['From'] = gmail_user
		msg['To'] = to
		if len(resrnt_df) == 0:
			html = """
			<html>
			<head>
			<style>
			table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
				width: 100%;
			}

			td {
				background-color: #0563AA;
				border: 1px solid #dddddd;
				text-align: left;
				padding: 8px;
			}
			
			th {
				background-color: #0563AA;
				color: white;
				border: 1px solid #dddddd;
				text-align: left;
				padding: 8px;
				}

			tr:nth-child(even) {
				background-color: #dddddd;
			}
			</style>
			</head>
			<body>
			<p>Hi!</p>
			<p>Thanks for using Foodie.</p>
			<p>Sorry, we could not find restaurant that meet your criteria.</p>
			"""
		else:
			resrnt_df10 = resrnt_df.head(10)
			resrnt_df10 = resrnt_df10.reset_index(drop=True)
			resrnt_df10.index = resrnt_df10.index.map(str)
			html = """
			<html>
			<head>
			<style>
			table {
				font-family: arial, sans-serif;
				border-collapse: collapse;
				width: 100%;
			}

			td, th {
				border: 1px solid #dddddd;
				text-align: left;
				padding: 8px;
			}

			tr:nth-child(even) {
				background-color: #dddddd;
			}
			</style>
			</head>
			<body>
			<p>Hi!</p>
			<p>Thanks for using Foodie. Please find the requested list of restaurants below.</p>
			"""	
			html = html+resrnt_df10.to_html()
		html = html+"<p> based on your query...</p>"+cuisine+" restaurants costing "+budget+" budget at "+loc+"</body></html>"
		part2 = MIMEText(html, 'html')
		msg.attach(part2)
		server = smtplib.SMTP_SSL('smtp.gmail.com',465)
		server.ehlo()
		server.login(gmail_user, gmail_password)
		server.sendmail(sent_from, to, msg.as_string())
		server.close()
		dispatcher.utter_message("Email Sent")
		return [SlotSet('email',email)]

		
class ActionRestarted(Action): 	
    def name(self): 		
        return 'action_restarted' 	
    def run(self, dispatcher, tracker, domain): 
        return[Restarted()] 
