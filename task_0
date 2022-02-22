import requests
from datetime import datetime

_api_key = 'DEMO_KEY'

def get_neo_list(start_date, end_date, params_list, date_limit = 5):
    # Near Earth Object LIST
    # https://api.nasa.gov/neo/rest/v1/feed?start_date=2015-09-07&end_date=2015-09-08&api_key=DEMO_KEY
    r = requests.request('GET',
            f"https://api.nasa.gov/neo/rest/v1/feed?start_date={str(start_date)}&end_date={str(end_date)}&api_key={_api_key}")
    if r.status_code == 200:
        data = r.json()
        neo_list = data.get('near_earth_objects')
        if neo_list:
            for _date, neo in neo_list.items():
                sort_index = set()
                dataframe = dict()
                idx = list()
                for neo_date in neo:
                    id = neo_date['neo_reference_id']
                    dataframe[id] = dict()
                    for param in params_list:
                        dataframe[id][param] = neo_date[param]
                    sort_index.add(neo_date['absolute_magnitude_h'])
                sort_index_list = list(sort_index)
                sort_index_list.sort(reverse=True)
                idx = sort_index_list[:date_limit]
                del sort_index_list
                del sort_index

                print('\n', _date)
                count = 0
                for i in idx:
                    for k, v in dataframe.items():
                        if count < date_limit:
                            if v['absolute_magnitude_h'] == i:
                                count += 1
                                print(f'{count} {k}:', dataframe[k])

                        else:
                            break
    else:
        print(r.status_code)
    pass


if __name__ == '__main__':
    start_date = datetime(2022, 2, 23).date()
    end_date = datetime(2022, 2, 23).date()
    params_list = ['name', 'absolute_magnitude_h', 'is_potentially_hazardous_asteroid']
    date_limit = 12 # Количество объектов за каждую дату

    get_neo_list(start_date, end_date, params_list, date_limit)

