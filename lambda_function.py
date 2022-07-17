import os
import io
import boto3
import json
import csv

# grab environment variables
ENDPOINT_NAME = 'linear-learner-2022-07-13-12-26-49-522'
runtime= boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    
    data = json.loads(json.dumps(event))
    payload = data['data']
    print(payload)
    
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)
    print(response)
    result = json.loads(response['Body'].read().decode())
    print(result)
    pred = int(result['predictions'][0]['score'])
    predicted_label = 'yes' if pred >= 0 else 'no'
    
    return predicted_label