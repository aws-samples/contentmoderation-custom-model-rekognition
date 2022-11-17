import json
import urllib.parse
import boto3

rekognition = boto3.client('rekognition')
dynamodb = boto3.client('dynamodb')
mediaconvert_client = boto3.client(
    'mediaconvert', endpoint_url="https://mqm13wgra.mediaconvert.us-east-2.amazonaws.com")


def content_moderation(bucket, key):

    response = rekognition.start_content_moderation(
        Video={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        NotificationChannel={
            'SNSTopicArn': 'arn:aws:sns:us-east-2:123456789012:testtopic',
            'RoleArn': 'arn:aws:iam::123456789012:role/aws-rekognition'
        }
    )

    return response


def log_job_details(jobId, requestId):
    ddb_response = dynamodb.put_item(TableName='rekognition-demo-table',
                                     Item={
                                         "Id": {'S': jobId},
                                         "RequestId": {'S': requestId}
                                     }
                                     )

    return ddb_response


def start_mediaconvert_job(input_url, destination_url):
    response = mediaconvert_client.create_job(AccelerationSettings={
        'Mode': 'DISABLED'},
        # Add your AWS account number
        Queue="arn:aws:mediaconvert:us-east-2:123456789012:queues/Default",
        UserMetadata={},
        # Add media convert role ARN
        Role="arn:aws:iam::123456789012:role/service-role/MediaConvert_Default_Role",
        Settings={
        "TimecodeConfig": {
            "Source": "ZEROBASED"
        },
        "OutputGroups": [
            {
                "Name": "File Group",
                "Outputs": [
                    {
                        "ContainerSettings": {
                            "Container": "RAW"
                        },
                        "VideoDescription": {
                            "Width": 500,
                            "ScalingBehavior": "DEFAULT",
                            "Height": 500,
                            "TimecodeInsertion": "DISABLED",
                            "AntiAlias": "ENABLED",
                            "Sharpness": 50,
                            "CodecSettings": {
                                "Codec": "FRAME_CAPTURE",
                                "FrameCaptureSettings": {
                                    "FramerateNumerator": 1,
                                    "FramerateDenominator": 5,
                                    "MaxCaptures": 1,
                                    "Quality": 80
                                }
                            },
                            "DropFrameTimecode": "ENABLED",
                            "ColorMetadata": "INSERT"
                        },
                        "Extension": "jpg",
                        "NameModifier": "jpg"
                    },
                    {
                        "ContainerSettings": {
                            "Container": "MP4",
                            "Mp4Settings": {
                                "CslgAtom": "INCLUDE",
                                "CttsVersion": 0,
                                "FreeSpaceBox": "EXCLUDE",
                                "MoovPlacement": "PROGRESSIVE_DOWNLOAD",
                                "AudioDuration": "DEFAULT_CODEC_DURATION"
                            }
                        },
                        "VideoDescription": {
                            "ScalingBehavior": "DEFAULT",
                            "TimecodeInsertion": "DISABLED",
                            "AntiAlias": "ENABLED",
                            "Sharpness": 50,
                            "CodecSettings": {
                                "Codec": "H_264",
                                "H264Settings": {
                                    "InterlaceMode": "PROGRESSIVE",
                                    "ScanTypeConversionMode": "INTERLACED",
                                    "NumberReferenceFrames": 3,
                                    "Syntax": "DEFAULT",
                                    "Softness": 0,
                                    "GopClosedCadence": 1,
                                    "GopSize": 90,
                                    "Slices": 1,
                                    "GopBReference": "DISABLED",
                                    "SlowPal": "DISABLED",
                                    "EntropyEncoding": "CABAC",
                                    "Bitrate": 1000,
                                    "FramerateControl": "INITIALIZE_FROM_SOURCE",
                                    "RateControlMode": "CBR",
                                    "CodecProfile": "MAIN",
                                    "Telecine": "NONE",
                                    "MinIInterval": 0,
                                    "AdaptiveQuantization": "AUTO",
                                    "CodecLevel": "AUTO",
                                    "FieldEncoding": "PAFF",
                                    "SceneChangeDetect": "ENABLED",
                                    "QualityTuningLevel": "SINGLE_PASS",
                                    "FramerateConversionAlgorithm": "DUPLICATE_DROP",
                                    "UnregisteredSeiTimecode": "DISABLED",
                                    "GopSizeUnits": "FRAMES",
                                    "ParControl": "INITIALIZE_FROM_SOURCE",
                                    "NumberBFramesBetweenReferenceFrames": 2,
                                    "RepeatPps": "DISABLED",
                                    "DynamicSubGop": "STATIC"
                                }
                            },
                            "AfdSignaling": "NONE",
                            "DropFrameTimecode": "ENABLED",
                            "RespondToAfd": "NONE",
                            "ColorMetadata": "INSERT"
                        },
                        "AudioDescriptions": [
                            {
                                "AudioTypeControl": "FOLLOW_INPUT",
                                "AudioSourceName": "Audio Selector 1",
                                "CodecSettings": {
                                    "Codec": "AAC",
                                    "AacSettings": {
                                        "AudioDescriptionBroadcasterMix": "NORMAL",
                                        "Bitrate": 96000,
                                        "RateControlMode": "CBR",
                                        "CodecProfile": "LC",
                                        "CodingMode": "CODING_MODE_2_0",
                                        "RawFormat": "NONE",
                                        "SampleRate": 48000,
                                        "Specification": "MPEG4"
                                    }
                                },
                                "LanguageCodeControl": "FOLLOW_INPUT"
                            }
                        ],
                        "NameModifier": "mp4"
                    }
                ],
                "OutputGroupSettings": {
                    "Type": "FILE_GROUP_SETTINGS",
                    "FileGroupSettings": {
                        "Destination": destination_url
                    }
                }
            }
        ],
        "AdAvailOffset": 0,
        "Inputs": [
            {
                "AudioSelectors": {
                    "Audio Selector 1": {
                        "Offset": 1,
                        "DefaultSelection": "DEFAULT",
                        "SelectorType": "TRACK",
                        "ProgramSelection": 1
                    }
                },
                "VideoSelector": {
                    "ColorSpace": "FOLLOW",
                    "Rotate": "DEGREE_0",
                    "AlphaBehavior": "DISCARD"
                },
                "FilterEnable": "AUTO",
                "PsiControl": "USE_PSI",
                "FilterStrength": 0,
                "DeblockFilter": "DISABLED",
                "DenoiseFilter": "DISABLED",
                "InputScanType": "AUTO",
                "TimecodeSource": "ZEROBASED",
                "FileInput": input_url
            }
        ]},
        StatusUpdateInterval="SECONDS_60",
        Priority=0)

    return response


def lambda_handler(event, context):

    data = json.dumps(event)

    # Extract the Object location metadata from the Lambda event
    bucket = event['Records'][0]['s3']['bucket']['name']
    print("S3 bucket is", bucket)
    key = urllib.parse.unquote_plus(
        event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print("S3 file is", key)

    # Start Content moderation Job. Use SNS Topic to notify job status
    rek_response = content_moderation(bucket, key)

    jobId = rek_response['JobId']
    requestId = rek_response['ResponseMetadata']['RequestId']

    # log the job details to DynamoDB
    ddb_response = log_job_details(jobId, requestId)
    print(json.dumps(ddb_response))

    # First Lambda function is used to trigger video workflow. This function is triggered by uploading car video file (example mp4) to S3.
    # Elemental media convert job is triggered to capture image frames and store image results in destination S3 bucket.

    # To find your "elemental media convert" region speicifc endpoint check => https://docs.aws.amazon.com/general/latest/gr/mediaconvert.html, Here we have ohio region.

    # original request made from console
    #input_url = "s3://car-video-feed-001/input/video-1.mp4"
    #destination_url = "s3://car-video-feed-001/output/"
    bucket_info = event["Records"][0]["s3"]
    bucket_name = bucket_info["bucket"]["name"]
    bucket_object = bucket_info["object"]["key"]

    input_url = "s3://"+bucket_name+"/"+bucket_object
    # It is destination S3 bucket used to store output of elemental media convert job. Output consists of images & parent video file. where "Video_inputs" is S3 prefix, used to store output image(s).
    destination_url = "s3://customlabel-destination/video_inputs/"

    response = start_mediaconvert_job(input_url, destination_url)
    print(response)

    return {
        'statusCode': 200,
        'body': json.dumps(ddb_response)
    }
