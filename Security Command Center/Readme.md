# Notification to Teams Function

## Overview

This repository contains a Python script for sending notifications from Google Security Command Center (SCC) to Microsoft Teams. Originally inspired by Google's SCC documentation on enabling real-time email and chat notifications, this script has been adapted to work with Microsoft Teams, providing an alternative to Slack, Email, and Webex notifications.

The script is designed to be deployed as a Google Cloud Function and listens for messages on a Google Cloud Pub/Sub topic, which are then forwarded to a Microsoft Teams channel.

Reference Documentation: [[Enabling real-time email and chat notifications | Security Command Center | Google Cloud](https://cloud.google.com/security-command-center/docs/how-to-enable-real-time-notifications#sendgrid-email)]

## Prerequisites

- Google Cloud account with access to Security Command Center.
- A Microsoft Teams channel and permissions to set up incoming webhooks.
- Google Cloud SDK (`gcloud`) installed and configured for command-line usage.
- Forwarded event notification from Security Command Center to a pub/sub topic

## Customizing Notification Content

The notification's content can be tailored to include specific fields from SCC findings. To explore the available fields in the SCC notification messages, use the following `gcloud` commands:

```jsx
gcloud scc notifications list 123
gcloud scc notifications list organizations/123
```

Replace **`123`** with your organization's ID. These commands will help you identify the JSON structure of SCC notifications, allowing you to customize which information is included in the Teams message.

## **Microsoft Teams Webhook Format**

The payload sent to the Microsoft Teams webhook must be in a format that Teams understands – typically a JSON payload structured as a [Message Card](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using?tabs=cURL). Ensure that the script formats the message data correctly to match Microsoft Teams' expected layout for message cards.

## **Setup and Deployment**

1. **Create a Microsoft Teams Webhook:**
    - In your Microsoft Teams channel, create an incoming webhook and note the URL.
2. **Modify the Script:**
    - In the script, replace the **`webhook_url`** variable with your Microsoft Teams webhook URL.
3. **Deploy the Cloud Function:**
    - From the root directory of your cloned repository, run the following **`gcloud`** command:
        
        ```css
        gcloud functions deploy hello_pubsub \
          --runtime python38 \
          --trigger-topic YOUR_PUBSUB_TOPIC_NAME \
          --entry-point hello_pubsub
        
        ```
        
        Replace **`YOUR_PUBSUB_TOPIC_NAME`** with the name of the Pub/Sub topic that SCC sends notifications to.
        
4. **Test the Function:**
    - Trigger a test notification in SCC or publish a test message to your Pub/Sub topic.
    - Verify that the notification appears correctly in your Microsoft Teams channel.