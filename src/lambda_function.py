import os
import boto3
import json

def create_case(event):
    # Support endpoint is only available on us-east-1 - https://docs.aws.amazon.com/general/latest/gr/awssupport.html
    client = boto3.setup_default_session(region_name='us-east-1')
    
    # Creates the client to connect to the Support API
    client = boto3.client('support')
    
    # Saving the account ID of new account into $new_account
    new_account = event["detail"]["serviceEventDetails"]["createAccountStatus"]["accountId"]
    
    # For the record on logs
    print(f'New account ID is: { new_account }')
    
    # Gets the New Account ID from the event and submit the support case
    
    try:
        response = client.create_case(
            subject=f'Please enable Enterprise Support for account { new_account }',
            severityCode='high',
            communicationBody=f'Please enable Enterprise Support on newly created account { new_account }',
            issueType='customer-service'
        )
    
        print(f"Support case created for account {new_account}")

    except:
        print("Something went wrong and support case was not created.")
    
def lambda_handler(event, context):
    # Starting execution
    create_case(event)
