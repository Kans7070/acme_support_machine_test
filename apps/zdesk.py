import requests as req

from django.conf import settings

def ticket_show():
    data = req.get(settings.ZENDESK_TICKETS_DOMAIN,auth=(settings.ZENDESK_EMAIL,settings.ZENDESK_PASSWORD))
    print(data.json())
    return data.json()