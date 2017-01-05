# quick and dirty as well...
import requests

def log_power(value, uuid, *args, **kwargs):
    address = kwargs.get('address', '127.0.0.1')
    port = kwargs.get('port', 80)
    timestamp = kwargs.get('timestamp', None)
    protocol = kwargs.get('protocol', 'http')
    url = "{protocol}://{address}:{port}/middleware.php/data/{uuid}.json?value={value}".format(protocol=protocol, address=address, port=port, uuid=uuid, value=value)
    if timestamp:
        url += "&timestamp={timestamp}".format(timestamp=timestamp)
    try:
        response = requests.post(url, timeout=5)
    except Exception as e:
        raise e
    if response.status_code != 200:
        print(response)
        raise MiddlewareException("Status Code was {} for {}".format(response.status_code, response.url))
    return response

class MiddlewareException(Exception):
    pass
