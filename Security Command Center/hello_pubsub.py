import base64
import json
import requests

def hello_pubsub(event, context):
    """Triggered from a message on a Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    # Decode the message from the Pub/Sub event
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_json = json.loads(pubsub_message)

    # Extract the description
    description = message_json['finding']['description']

    # Extract the first offending IAM role email from iamBindings, if available
    iam_bindings = message_json['finding'].get('iamBindings', [])
    first_offending_email = iam_bindings[0]['member'] if iam_bindings else 'N/A'

    # Construct the Microsoft Teams message card
    teams_message = {
        "@type": "MessageCard",
        "@context": "http://schema.org/extensions",
        "themeColor": "0076D7",
        "summary": "New High or Critical Severity Finding Detected",
        "sections": [{
            "activityTitle": "**New Finding Detected**",
            "activitySubtitle": description,
            "facts": [
                {"name": "Category", "value": message_json['finding']['category']},
                {"name": "Severity", "value": message_json['finding']['severity']},
                {"name": "Offending Email", "value": first_offending_email}
            ],
            "markdown": True
        }],
        "potentialAction": [{
            "@type": "OpenUri",
            "name": "View in GCP Console",
            "targets": [{"os": "default", "uri": message_json['finding']['externalUri']}]
        }]
    }

    # Webhook URL for Microsoft Teams
    webhook_url = 'https://wowrack.webhook.office.com/webhookb2/fbc36d86-84f0-4e34-9dab-4fed531e7fc2@56454c92-3748-402b-ac74-345d7c6bb8b2/IncomingWebhook/c500b260dbab4c38b1eef150b4e3f4c1/45724664-9f0a-4d04-b8ec-3e7739b01428'

    # Send the POST request to the Microsoft Teams webhook URL
    try:
        response = requests.post(webhook_url, json=teams_message)
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending to Microsoft Teams webhook:", e)

    # Optionally print the received Pub/Sub message
    print(pubsub_message)