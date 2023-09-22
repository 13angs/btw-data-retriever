import requests, json, os, time, math, random
from dotenv import load_dotenv

# Load environment variables from a `.env` file.
load_dotenv()

# Retrieve neccessary environment variables.
API_URL = os.environ['API_URL']
STORE_ID = os.environ['STORE_ID']
LIMIT = os.environ['LIMIT']
IS_BACKEND = os.environ['IS_BACKEND']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

# Initialize the current_page variable to 1.
current_page = 1

# Construct the full URL for the API request using environment variables.
full_url = f'{API_URL}/productlist?store_id={STORE_ID}&limit=1&page={current_page}&is_backend={IS_BACKEND}'

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}'
}

# Send the first HTTP GET request to the API.
response = requests.get(url=full_url, headers=headers)

# Initialize the total_data variable to 0.
total_data = 0

# Check if the API response status code is 200 (OK).
if response.status_code == 200:

    json_response = response.json()

    # Extract the 'total' field from the response data.
    total_data = json_response['data']['total']
    
    print('Total data: ', total_data)
else:
    # If the response status code is not 200, raise an exception.
    err_msg = f'Failed to fetch data from API. Status code: {response.status_code}'
    print(err_msg)
    raise Exception(err_msg)

print('Start fetching products...')

# Reset the current_page variable to 1.
current_page = 1

# Initialize the final_data variable to 0.
final_data = 0

# Calculate the threshold page based on total data and limit.
threshold_page = math.ceil(total_data / int(LIMIT))

# Specify the file name for storing product data as a JSON file.
file_name = 'data/products.json'

# Start a while loop for fetching data until the final_data matches total_data.
while True:

    print(f'Fetching {LIMIT} products from page {current_page}...')
    
    # Construct the full URL for the API request with updated page and limit.
    full_url = f'{API_URL}/productlist?store_id={STORE_ID}&limit={LIMIT}&page={current_page}&is_backend={IS_BACKEND}'
    
    # Send an HTTP GET request to the API with the updated URL and headers.
    response = requests.get(url=full_url, headers=headers)

    # Check if the API response status code is not 200.
    if response.status_code != 200:
        err_msg = f'Failed to fetch data from API. Status code: {response.status_code}'
        raise Exception(err_msg)

    json_response = response.json()

    # Extract the list of products from the response data.
    products = json_response['data']['product_list']

    # Try to open the existing JSON file for appending data.
    try:
        with open(file_name, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist yet, initialize existing_data as an empty list.
        existing_data = []

    # Append the newly fetched products to the existing data.
    existing_data.extend(products)

    # Write the updated data to the JSON file.
    with open(file_name, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

    print(f'Successfully append products in {file_name}')

    # Generate a random sleep duration between 5 and 10 seconds.
    sec = random.randrange(5, 10)
    print(f'Rest for {sec} seconds...')
    
    time.sleep(sec)

    # Increment the current_page counter.
    current_page += 1

    # Update the final_data count based on the length of existing_data.
    final_data = len(existing_data)

    # Check if final_data matches total_data, and exit the loop if they are equal.
    if total_data == final_data:
        break
    elif final_data > total_data:
        # Raise an exception if final_data exceeds total_data (an unexpected condition).
        raise Exception("Please recheck the code. The final_data shouldn't be greater than total_data!")

print(f'Finish fetching {final_data} products!')