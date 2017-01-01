# quick and dirty
# TODO: proper fronius JSON API client
import requests

def get_power(ip, device_id=1):
    try:
        response = requests.get('http://{ip}/solar_api/v1/GetInverterRealtimeData.cgi?Scope=Device&DeviceId={device_id}&DataCollection=CommonInverterData'.format(ip=ip, device_id=device_id))
    except requests.exceptions.ConnectionError:
        raise InverterException("Inverter unavailable (Sleeping?)")
    try:
        power = response.json()['Body']['Data']['PAC']['Value']
    except KeyError:
        pass  # inverter power stage shut down
        raise InverterException("Power Stage probably shut down")
    return power

class InverterException(Exception):
    pass
