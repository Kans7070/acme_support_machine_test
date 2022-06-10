import json
import requests as req

from django.conf import settings


def ticket_show():
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
    