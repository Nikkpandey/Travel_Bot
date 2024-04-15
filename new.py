import csv
import random
import re

# Define responses for different types of user inputs
GREETING_RESPONSES = ["Hello! Welcome to the Travel Bot.", "Hi there! How can I assist you today?", "Hey! Ready to plan your next adventure?"]
GOODBYE_RESPONSES = ["Goodbye! Have a great day!", "See you later! Happy travels!", "Farewell!"]
ERROR_RESPONSES = ["I'm sorry, I didn't quite catch that.", "Could you please rephrase that?", "Apologies, I didn't understand."]
THANKS_RESPONSES = ["You're welcome!", "My pleasure!", "Glad I could help!"]
UNKNOWN_DESTINATION_RESPONSE = "Sorry, I couldn't find any information about that destination. Where else would you like to go?"

# Read data from CSV file
def read_csv_file(file_name):
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [row for row in reader]
    return data

# Retrieve information about a random destination
def get_destination_info(data):
    destinations = [row for row in data if row['Category'] == 'Destination']
    destination = random.choice(destinations)
    return {
        'name': destination['Name'],
        'description': destination['Description'],
        'image': destination['Image']
    }

# Retrieve information about a random flight
def get_flight_info(data, source):
    flights = [row for row in data if row['Category'] == 'Flight' and row['Source'].lower() == source.lower()]
    if flights:
        flight = random.choice(flights)
        return {
            'airline': flight['Airline'],
            'destination': flight['Destination'],
            'departure_time': flight['Departure Time'],
            'arrival_time': flight['Arrival Time'],
            'price': flight['Price']
        }
    else:
        return None

# Retrieve information about a random hotel in a location
def get_hotel_info(data, location):
    hotels = [row for row in data if row['Category'] == 'Hotel' and row['Location'].lower() == location.lower()]
    if hotels:
        hotel = random.choice(hotels)
        return {
            'name': hotel['Name'],
            'price': hotel['Price'],
            'rating': hotel['Rating'],
            'image': hotel['Image']
        }
    else:
        return None

# Handle user input and generate a response
def generate_response(user_input, data):
    user_input = user_input.lower()

    # Check if user input contains greetings
    if any(greet_word in user_input for greet_word in ['hello', 'hi', 'hey']):
        return random.choice(GREETING_RESPONSES)

    # Check if user input contains goodbye keywords
    elif any(bye_word in user_input for bye_word in ['bye', 'goodbye']):
        return random.choice(GOODBYE_RESPONSES)

    # Check if user input contains thanks keywords
    elif 'thank' in user_input:
        return random.choice(THANKS_RESPONSES)

    # Check if user input contains destination query
    elif 'suggest me a place to travel' in user_input:
        destination = get_destination_info(data)
        return f"How about visiting {destination['name']}? {destination['description']}"

    # Check if user input contains flight query
    elif 'show me flights to' in user_input:
        source = re.search(r"show me flights to (.+)", user_input).group(1)
        flight_info = get_flight_info(data, source)
        if flight_info:
            return f"Here's a flight from {source} to {flight_info['destination']} with {flight_info['airline']}. Departure time: {flight_info['departure_time']}, Arrival time: {flight_info['arrival_time']}, Price: {flight_info['price']}"
        else:
            return "Sorry, we don't have any flights from that location."

    # Check if user input contains hotel query
    elif 'find me a hotel in' in user_input:
        location = re.search(r"find me a hotel in (.+)", user_input).group(1)
        hotel_info = get_hotel_info(data, location)
        if hotel_info:
            return f"Here's a hotel in {location}: {hotel_info['name']}. Price: {hotel_info['price']}, Rating: {hotel_info['rating']}"
        else:
            return "Sorry, we don't have any hotels in that location."

    # If none of the above conditions are met, respond with an error message
    else:
        return random.choice(ERROR_RESPONSES)

# Main function to interact with the user
def main():
    data = read_csv_file('data.csv')
    print(random.choice(GREETING_RESPONSES))
    while True:
        user_input = input("How can I assist you today? (Type 'exit' to end the conversation)\n")
        if user_input.lower() == 'exit':
            print(random.choice(GOODBYE_RESPONSES))
            break
        else:
            response = generate_response(user_input, data)
            print(response)

if __name__ == "__main__":
    main()
