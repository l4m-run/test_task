from json import JSONDecodeError
import requests
import datetime

NASA_API_URL = 'https://api.nasa.gov/neo/rest/v1/feed'
API_KEY = 'DEMO_KEY'
OBJ_KEYS = ['name', 'absolute_magnitude_h', 'is_potentially_hazardous_asteroid']


def get_data_neo_from_nasa_api(start_date, end_date, api_key):
    """
    Забираем данные о близлежащих к земле объектах из api NASA
    :param start_date: дата начала
    :param end_date: дата окончания
    :param api_key: api ключ
    :return: Ответ в формате requests.response
    """

    url = NASA_API_URL
    params = {
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d"),
        'api_key': api_key
    }

    data = requests.get(url=url, params=params)

    return data


def prepare_data_to_print(data):
    """
    Подготавливаем данные к печати. Данные должны быть в формате dict.
    При подготовке данные записываются в нужный формат и сортируются.
    :param data: данные для сортировки.
    :return: Отсортированный словарь в нужном формате.
    """
    if type(data) != dict:
        raise ValueError
    element_count = int(data["element_count"])
    near_earth_objects = data["near_earth_objects"]
    objects_dict = {}
    for date, values in near_earth_objects.items():
        for obj in values:
            key = f'{date} {obj["neo_reference_id"]}'
            objects_dict[key] = {x: obj[x] for x in OBJ_KEYS}
    return element_count, objects_dict


def print_objects_near_earth(start_date, end_date, limit):
    if start_date.date() > end_date.date():
        print("Error: start_date should be earlier or same as end_date")
        return

    # Получаем данные из api.
    try:
        response = get_data_neo_from_nasa_api(start_date, end_date, API_KEY)
    except requests.RequestException as err:
        print(f"Error: {err}")
        return
    if not response.ok:
        print(f"Error in response: response status code is {response.status_code}")
        return
    try:
        data = response.json()
    except JSONDecodeError:
        print(f"Error: wrong response format. {response.content}")
        return

    # Форматируем данные.
    element_count, objects_near_earth_dict = prepare_data_to_print(data)
    sorted_objects = sorted(objects_near_earth_dict.items(), key=lambda item: item[1]["absolute_magnitude_h"],
                            reverse=True)

    # Печатаем
    length = min(limit, element_count)
    for i in range(length):
        print(sorted_objects[i])


if __name__ == '__main__':
    print_objects_near_earth(datetime.datetime(2022, 2, 23), datetime.datetime(2022, 2, 23), 7)
