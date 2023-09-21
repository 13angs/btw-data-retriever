import requests, json, os, time, math, random
from dotenv import load_dotenv

load_dotenv()

API_URL = os.environ['API_URL']
STORE_ID = os.environ['STORE_ID']
LIMIT = os.environ['LIMIT']
IS_BACKEND = os.environ['IS_BACKEND']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']

current_page=1

full_url = f'{API_URL}/productlist?store_id={STORE_ID}&limit=1&page={current_page}&is_backend={IS_BACKEND}'

headers = {
    'Authorization' : f'Bearer {ACCESS_TOKEN}'
}

response = requests.get(url=full_url, headers=headers)

total_data=0

if response.status_code == 200:
    json_response = response.json()

    total_data = json_response['data']['total']
    print('Total data: ', total_data)
else:
    err_msg = f'Failed to fetch data from API. Status code: {response.status_code}'
    print(err_msg)
    raise Exception(err_msg)

print('Start fetching products...')


current_page=1
final_data=0
threshold_page=math.ceil(total_data / int(LIMIT))
file_name='data/products.json'

while True:
    print(f'Fetching {LIMIT} products from page {current_page}...')
    
    full_url = f'{API_URL}/productlist?store_id={STORE_ID}&limit={LIMIT}&page={current_page}&is_backend={IS_BACKEND}'
    response = requests.get(url=full_url, headers=headers)

    if response.status_code != 200:
        err_msg = f'Failed to fetch data from API. Status code: {response.status_code}'
        raise Exception(err_msg)

    json_response = response.json()

    products = json_response['data']['product_list']

    try:
        with open(file_name, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(products)

    with open(file_name, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4, ensure_ascii=False)

    print(f'Successfully append products in {file_name}')

    sec = random.randrange(5, 10)
    print(f'Rest for {sec} seconds...')
    time.sleep(sec)


    current_page+=1

    final_data=len(existing_data)

    if(total_data == final_data):
        break
    elif (final_data > total_data):
        raise Exception("Please recheck the code. The final_data shouldn't be greater that total_data!")

print(f'Finish fetching {final_data} products!')