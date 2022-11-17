import json
import boto3

client = boto3.client('rekognition')
s3 = boto3.resource('s3')
dynamodb = boto3.client('dynamodb')


def get_content_moderation_job_details(jobinfo):
    rek_response = client.get_content_moderation(
        JobId=jobinfo,
        MaxResults=100,
        SortBy='TIMESTAMP')

    return rek_response


def moderation_logging_to_dynamodb(src_object, rek_response, i):
    ddb_response = dynamodb.put_item(TableName='Censored',
                                     Item={
                                         "Video": {'S': src_object},
                                         "Confidence": {'S': str(rek_response['ModerationLabels'][i]['ModerationLabel']['Confidence'])},
                                         "Name": {'S': rek_response['ModerationLabels'][i]['ModerationLabel']['Name']}
                                     }
                                     )
    return ddb_response


def lambda_handler(event, context):
    data = json.dumps(event)

    message = event['Records'][0]['Sns']['Message']
    mesageJson = json.loads(message)

    jobinfo = mesageJson['JobId']
    print(jobinfo)

    rek_response = get_content_moderation_job_details(jobinfo)

    print(json.dumps(rek_response['ModerationLabels']))

    src_bucket = mesageJson["Video"]["S3Bucket"]
    src_object = mesageJson["Video"]["S3ObjectName"]

    length = len(rek_response)
    for i in range(0, length):
        print(rek_response['ModerationLabels'][i]
              ['ModerationLabel']['Confidence'])
        ddb_response = moderation_logging_to_dynamodb(
            src_object, rek_response, i)

    if (len(rek_response["ModerationLabels"])):
        copy_source = {
            'Bucket': src_bucket,
            'Key': src_object
        }
        s3.meta.client.copy(copy_source, 'moderationfinal', src_object)
    else:
        print("no labels found")

    return {
        'statusCode': 200,
        'body': json.dumps('success')
    }
