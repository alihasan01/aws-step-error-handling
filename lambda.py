import json
import boto3

step_functions = boto3.client('stepfunctions')
s3_client = boto3.resource('s3')

def lambda_handler(event, context):
    # TODO implement

    print(event)
    task_token = event['token']
    try:
        bucket = event['input']['bucket']
        fileName = event['input']['key']
        obj = s3_client.Object(bucket, fileName)
        s3response = obj.get()
        data = s3response['Body'].read().decode('utf-8')

        step_functions.send_task_success(
            taskToken=task_token,
            output=json.dumps({"data" : json.loads(data) }
        ))
    except Exception as error:
        step_functions.send_task_failure(
            taskToken=task_token,
            error='error',
            cause= str(error) + " bucket: "  + bucket +  " file: " + fileName
        )
        