import boto3
import json
import urllib.parse
client = boto3.client('rekognition')
s3 = boto3.resource('s3')


def custom_labels_detection(bucket, key):
    response = client.detect_custom_labels(
        ProjectVersionArn='arn:aws:rekognition:us-east-2:123456789012:project/test-dataset-ab2/version/test-dataset-ab2.2022-06-18T16.40.55/1655550655515',
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key

            }
        },
        MaxResults=123,
        MinConfidence=80
    )
    return response


def lambda_handler(event, context):

    data = json.dumps(event)

   # Extract the Object location metadata from the Lambda event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("S3 bucket is", bucket)

    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("S3 file is", key)

    response = custom_labels_detection(bucket, key)
    print(response)

    key1 = key.split("jpg")[0]+".mp4"
    final_key = key1.split("/")[1]
    print(key1)

    if (len(response["CustomLabels"])):
        copy_source = {
            'Bucket': 'aws-rekognition-bucketxx',
            'Key': final_key
        }
        s3.meta.client.copy(copy_source, 'plagiarismchecker', final_key)
    else:
        print("no labels found")

    return {
        'statusCode': 200,
        'body': json.dumps('response')
    }
