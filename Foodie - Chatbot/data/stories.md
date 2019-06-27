## Complete story in a sequence
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
	- slot{"location": "delhi"}
 	- action_validate_location
 	- slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
	- slot{"cuisine": "North Indian"}
    - action_validate_cuisine
 	- slot{"cuisine": "North Indian"}
	- utter_ask_budget
* restaurant_search{"budget": "Lesser than Rs 300"}
    - slot{"budget": "Lesser than Rs 300"}
	- action_validate_budget
	- slot{"budget": "low"}
	- utter_top_restaurant
	- action_restaurant
    - slot{"budget": "low"}
 	- utter_ask_about_emailing
* affirm
    - utter_ask_email_id
* send_email{"email": "selvaganapathyu@outlook.com"}
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_validate_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- utter_goodbye
    - action_restarted

## Complete story in a sequence - User does not need email option
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
	- slot{"location": "delhi"}
 	- action_validate_location
 	- slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
	- slot{"cuisine": "North Indian"}
    - action_validate_cuisine
 	- slot{"cuisine": "North Indian"}
	- utter_ask_budget
* restaurant_search{"budget": "Lesser than Rs 300"}
    - slot{"budget": "Lesser than Rs 300"}
	- action_validate_budget
	- slot{"budget": "low"}
	- utter_top_restaurant
	- action_restaurant
    - slot{"budget": "low"}
 	- utter_ask_about_emailing
* deny
    - utter_goodbye
    - action_restarted


## Complete story in a sequence - User provides Unknown city (Out of Tier 1 and 2).
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "Vellore"}
	- slot{"location": "Vellore"}
    - action_validate_location
	- slot{"location": null}
    - utter_ask_location 
* restaurant_search{"location": "delhi"}
	- slot{"location": "delhi"}
 	- action_validate_location
 	- slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
	- slot{"cuisine": "North Indian"}
    - action_validate_cuisine
 	- slot{"cuisine": "North Indian"}
	- utter_ask_budget
* restaurant_search{"budget": "Lesser than Rs 300"}
    - slot{"budget": "Lesser than Rs 300"}
	- action_validate_budget
	- slot{"budget": "low"}
	- utter_top_restaurant
	- action_restaurant
    - slot{"budget": "low"}
 	- utter_ask_about_emailing
* affirm
    - utter_ask_email_id
* send_email{"email": "selvaganapathyu@outlook.com"}
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_validate_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- utter_goodbye
    - action_restarted	

	
## Complete story in a sequence - User provides Unknown Cuisine.
* greet
    - utter_greet
* greet
    - utter_greet
* restaurant_search
    - utter_ask_location
* restaurant_search{"location": "delhi"}
	- slot{"location": "delhi"}
	- action_validate_location
	- slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "Japanese"}
	- slot{"cuisine": "Japanese"}
	- action_validate_cuisine
	- slot{"cuisine": null}
	- utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
	- slot{"cuisine": "North Indian"}
	- action_validate_cuisine
	- slot{"cuisine": "North Indian"}
	- utter_ask_budget
* restaurant_search{"budget": "Lesser than Rs 300"}
    - slot{"budget": "Lesser than Rs 300"}
	- action_validate_budget
	- slot{"budget": "low"}
	- utter_top_restaurant
	- action_restaurant
    - slot{"budget": "low"}
 	- utter_ask_about_emailing
* affirm
    - utter_ask_email_id
* send_email{"email": "selvaganapathyu@outlook.com"}
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_validate_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- utter_goodbye
    - action_restarted		
	

## User provided Location Initially
* greet
    - utter_greet
* restaurant_search{"location": "delhi"}
	- slot{"location": "delhi"}
 	- action_validate_location
 	- slot{"location": "delhi"}
    - utter_ask_cuisine
* restaurant_search{"cuisine": "North Indian"}
	- slot{"cuisine": "North Indian"}
    - action_validate_cuisine
 	- slot{"cuisine": "North Indian"}
	- utter_ask_budget
* restaurant_search{"budget": "Lesser than Rs 300"}
    - slot{"budget": "Lesser than Rs 300"}
	- action_validate_budget
	- slot{"budget": "low"}
	- utter_top_restaurant
	- action_restaurant
    - slot{"budget": "low"}
 	- utter_ask_about_emailing
* affirm
    - utter_ask_email_id
* send_email{"email": "selvaganapathyu@outlook.com"}
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_validate_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- action_email
 	- slot{"email": "selvaganapathyu@outlook.com"}
 	- utter_goodbye
    - action_restarted
	

## User doesnot need help (Deny)
* greet
    - utter_greet
* deny
    - utter_default
* deny
    - utter_goodbye
	- action_restarted