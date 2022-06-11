import json
import requests as req
from django.contrib import messages


from django.conf import settings


def ticket_show(email=None):
    if email:
        data = req.get(url=settings.ZENDESK_TICKETS_DOMAIN , auth=(
        settings.ZENDESK_EMAIL, settings.ZENDESK_PASSWORD))
        sorted_data =[]
        for i in data.json()['tickets']:
            if i['custom_fields'][0]['value'] == email:
                sorted_data.append(i)
        return sorted_data
    data = req.get(url=settings.ZENDESK_TICKETS_DOMAIN, auth=(
        settings.ZENDESK_EMAIL, settings.ZENDESK_PASSWORD))
    
    return data.json()


def create_ticket(data):
    data = {
        'ticket':data
    }
    data = req.post(url=settings.ZENDESK_TICKETS_DOMAIN, auth=(
        settings.ZENDESK_EMAIL, settings.ZENDESK_PASSWORD),headers={"Content-Type": "application/json"},data=json.dumps(data))


def create_user(data):
    data = {
        'user': data
    }
    data = req.post(url=settings.ZENDESK_USERS_DOMAIN, auth=(
        settings.ZENDESK_EMAIL, settings.ZENDESK_PASSWORD),headers={"Content-Type": "application/json"},data=json.dumps(data))
    return data.json()['user']['id']

def delete_ticket(id):
    req.delete(url=settings.ZENDESK_TICKETS_DOMAIN+id,auth=(settings.ZENDESK_EMAIL, settings.ZENDESK_PASSWORD))
    