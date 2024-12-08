import requests

# Ersetze diese Werte durch deine eigenen
API_URL = 'https://ifyouchange42862.api-us1.com/api/3'
API_KEY = 'a8bb1fd8ba76b2b1a0c2c58b1745ba2fc458e5f69da898048ccd790b14a5206db1bd9ef7'

headers = {
    'Api-Token': API_KEY,
    'Content-Type': 'application/json'
}

# Ersetze durch deine Formular-Action-URL
FORM_ACTION_URL = 'https://ifyouchange42862.activehosted.com/f/25'


# 1. Kontakt anhand der E-Mail-Adresse abrufen
def get_contact_by_email(email):
    params = {
        'email': email
    }
    response = requests.get(f"{API_URL}/contacts", params=params, headers=headers)
    data = response.json()
    if 'contacts' in data and len(data['contacts']) > 0:
        return data['contacts'][0]
    else:
        return None

# 2. Kontakt erstellen oder vorhandenen Kontakt abrufen
def create_or_get_contact(email):
    contact = get_contact_by_email(email)
    if contact:
        print(f"Kontakt mit E-Mail {email} existiert bereits.")
        return contact
    else:
        data = {
            "contact": {
                "email": email
            }
        }
        response = requests.post(f"{API_URL}/contacts", json=data, headers=headers)
        data = response.json()
        if 'contact' in data:
            return data['contact']
        else:
            print(f"Fehler beim Erstellen des Kontakts: {data}")
            return None

# 3. Liste anhand des Namens abrufen
def get_list_by_name(list_name):
    response = requests.get(f"{API_URL}/lists", headers=headers)
    data = response.json()
    if 'lists' in data:
        for liste in data['lists']:
            if liste['name'] == list_name:
                return liste
    return None

# 4. Liste erstellen oder vorhandene Liste abrufen
def create_or_get_list(list_name):
    liste = get_list_by_name(list_name)
    if liste:
        print(f"Liste mit Namen '{list_name}' existiert bereits.")
        return liste
    else:
        data = {
            "list": {
                "name": list_name,
                "stringid": list_name.lower().replace(' ', '_'),
                "sender_url": "https://ifyouchange42862.activehosted.com/",
                "sender_reminder": "Du erhältst diese E-Mail, weil du dich auf unserer Website angemeldet hast."
            }
        }
        response = requests.post(f"{API_URL}/lists", json=data, headers=headers)
        data = response.json()
        if 'list' in data:
            return data['list']
        else:
            print(f"Fehler beim Erstellen der Liste: {data}")
            return None

# 5. Kontakt zur Liste hinzufügen
def add_contact_to_list(contact_id, list_id):
    data = {
        "contactList": {
            "list": list_id,
            "contact": contact_id,
            "status": 1  # 1 für aktiviert
        }
    }
    response = requests.post(f"{API_URL}/contactLists", json=data, headers=headers)
    return response.json()


# 6. Nachricht anhand des Betreffs abrufen
def get_message_by_subject(subject):
    response = requests.get(f"{API_URL}/messages", headers=headers)
    data = response.json()
    if 'messages' in data:
        for message in data['messages']:
            if message['subject'] == subject:
                return message
    return None

# 7. Nachricht erstellen oder vorhandene Nachricht abrufen
def create_or_get_message(subject, from_email, from_name, html_content):
    message = get_message_by_subject(subject)
    if message:
        print(f"Nachricht mit Betreff '{subject}' existiert bereits.")
        return message
    else:
        data = {
            "message": {
                "subject": subject,
                "fromEmail": from_email,
                "fromName": from_name,
                "html": html_content,
                "generateText": True,
                "autoText": True
            }
        }
        response = requests.post(f"{API_URL}/messages", json=data, headers=headers)
        data = response.json()
        if 'message' in data:
            return data['message']
        else:
            print(f"Fehler beim Erstellen der Nachricht: {data}")
            return None

# 8. Kampagne anhand des Namens abrufen
def get_campaign_by_name(name):
    response = requests.get(f"{API_URL}/campaigns", headers=headers)
    data = response.json()
    if 'campaigns' in data:
        for campaign in data['campaigns']:
            if campaign['name'] == name:
                return campaign
    return None

# 9. Kampagne erstellen oder vorhandene Kampagne abrufen
def create_or_get_campaign(name, message_id, list_id):
    campaign = get_campaign_by_name(name)
    if campaign:
        print(f"Kampagne mit Namen '{name}' existiert bereits.")
        return campaign
    else:
        data = {
            "campaign": {
                "name": name,
                "message_id": message_id,
                "type": "single",
                "list_ids": [list_id],
                "status": 1  # 1 für Entwurf
            }
        }
        response = requests.post(f"{API_URL}/campaigns", json=data, headers=headers)
        if response.status_code == 403:
            print(f"Fehler beim Erstellen der Kampagne: {response.status_code} - {response.text}")
            print("Überprüfe die API-Berechtigungen und stelle sicher, dass dein API-Schlüssel die erforderlichen Rechte hat.")
            return None
        data = response.json()
        if 'campaign' in data:
            return data['campaign']
        else:
            print(f"Fehler beim Erstellen der Kampagne: {data}")
            return None


# 10. Kampagne senden
def send_campaign(campaign_id):
    response = requests.post(f"{API_URL}/campaigns/{campaign_id}/send", headers=headers)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        print(f"Fehler beim Senden der Kampagne: {response.status_code} - {data}")
        return None


def submit_form(email, first_name):
    form_url = 'https://ifyouchange42862.activehosted.com/proc.php'
    data = {
        'u': '25',
        'f': '25',
        's': '',
        'c': '0',
        'm': '0',
        'act': 'sub',
        'v': '2',
        'or': '1b8a5663599fc2cbe3a86b7a3d3f244c',  # Wert aus deinem Formular
        'firstname': first_name,
        'email': email
    }

    response = requests.post(form_url, data=data)
    if response.status_code == 200:
        print("Formular erfolgreich übermittelt. Double Opt-In E-Mail wurde gesendet.")
    else:
        print(f"Fehler beim Übermitteln des Formulars: {response.status_code} - {response.text}")


# Hauptprogramm
if __name__ == "__main__":
    email = 'sebastian.haug35@gmail.com'  # Ersetze durch deine E-Mail
    from_email = 'shmod35@gmail.com'  # Verifizierte Absender-E-Mail
    from_name = 'Sebastian'

    submit_form(email, from_name)

    # 1. Kontakt erstellen oder abrufen
    contact = create_or_get_contact(email)
    if contact is None:
        print("Kontakt konnte nicht erstellt oder abgerufen werden.")
        exit()

    contact_id = contact['id']

    # 2. Liste erstellen oder abrufen
    liste = create_or_get_list('Meine Liste')
    if liste is None:
        print("Liste konnte nicht erstellt oder abgerufen werden.")
        exit()

    list_id = liste['id']

    # 3. Kontakt zur Liste hinzufügen
    add_contact_to_list(contact_id, list_id)

    # 4. Nachricht erstellen oder abrufen
    html_content = '<p>Hallo, dies ist eine Test-E-Mail.</p>'
    message = create_or_get_message('Test E-Mail', from_email, from_name, html_content)
    if message is None:
        print("Nachricht konnte nicht erstellt oder abgerufen werden.")
        exit()

    message_id = message['id']

    # 5. Kampagne erstellen oder abrufen
    campaign = create_or_get_campaign('Meine Testkampagne', message_id, list_id)
    if campaign is None:
        print("Kampagne konnte nicht erstellt oder abgerufen werden.")
        exit()

    campaign_id = campaign['id']

    # 6. Kampagne senden
    send_response = send_campaign(campaign_id)
    if send_response is not None:
        print("E-Mail wurde erfolgreich gesendet!")
    else:
        print("Fehler beim Senden der E-Mail.")
