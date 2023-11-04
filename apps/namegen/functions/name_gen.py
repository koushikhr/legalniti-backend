import requests
from multiprocessing import Pool
from django.conf import settings

def fetch_names(offset, desc):
    url = "https://engine.renderforest.com/api/v1/business-name-suggestions"
    headers = {
        "Host": "engine.renderforest.com",
        "Origin": "https://www.renderforest.com",
        "Referer": "https://www.renderforest.com/business-name-suggestions",
    }
    data = {"description": desc, "limit": 20, "offset": offset}

    response = requests.post(url, headers=headers, data=data)
    return response.json().get('data', {}).get('names', [])
def fetch_distinct_names(desc):
    distinct_names = set()  # To store distinct names
    total_collected = 0
    desired_total = 20  # Target number of available names
    offset = 0

    with Pool(processes=settings.TOTAL_WORKER_THREAD) as pool:  # You can adjust the number of processes as needed
        while total_collected < desired_total:
            names = pool.starmap(fetch_names, [(offset, desc)] * settings.TOTAL_WORKER_THREAD)  # Fetch names in parallel
            
            for name_list in names:
                for name in name_list:
                    if name not in distinct_names:
                        distinct_names.add(name)
                        total_collected += 1

                        if total_collected >= desired_total:
                            break

            offset += 20

    return list(distinct_names)