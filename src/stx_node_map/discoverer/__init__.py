import logging
import requests

logging.basicConfig(level=logging.INFO)


def ip_to_location(ip: str):
    url = "https://freegeoip.app/json/{}".format(ip)
    try:
        resp = requests.get(url, timeout=5)
    except BaseException:
        return None

    if resp.status_code != 200:
        return None

    return resp.json()


def make_core_api_url(host: str):
    return "http://{}:20443/v2/neighbors".format(host)


def get_neighbors(host: str):
    url = make_core_api_url(host)

    try:
        json = requests.get(url, timeout=0.5).json()
    except BaseException:
        return []

    # collect all ip addresses
    all_ = [x["ip"] for x in json["sample"]] + [x["ip"] for x in json["inbound"]] + [x["ip"] for x in json["outbound"]]

    # make the list unique
    unique = list(set(all_))

    # skip local address
    return [a for a in unique if a != "0.0.0.0"]


found = []


def scan_list(list_):
    global found

    for address in list_:
        logging.info("Scanning {}".format(address))
        neighbors = get_neighbors(address)
        found += [n for n in neighbors if n not in found]


def worker():
    global found

    scan_list(get_neighbors("krypton.blockstack.org"))
    scan_list(found)

    logging.info("{} nodes found.".format(len(found)))
    logging.info("Detecting locations")

    result = []

    for address in found:
        neighbors = get_neighbors(address)
        location = ip_to_location(address)

        if len(neighbors) > 0 and location is not None:
            logging.info("{} is a public node".format(address))

            item = {
                "address": address,
                "location": {
                    "lat": location["latitude"],
                    "lng": location["longitude"],
                    "country": location["country_name"],
                    "city": location["city"]
                }
            }
        else:
            logging.info("{} is a private node".format(address))

            item = {
                "address": address
            }

        result.append(item)

    import pprint

    pprint.pprint(result)
