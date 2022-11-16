
README.md

A Video Content Moderation Technique with a Custom Model to identify the plagiarism in short Video Applications

When the short Video Applications cross millions of users, it becomes difficult to monitor, assess, and filter uploaded videos based on a predetermined set of rules. Content moderation technique is inevitable as it helps to maintain and enforce community guidelines.This Solution provides a Content Moderation pipeline that will ensure that their end-users are not exposed to potentially inappropriate or offensive material, such as nudity, violence, drug use, adult products, or disturbing images. Also it contains a Custom model to identify Plagiarism which means it helps you to identify any video being uploaded on to our application which is created using another platform. We tag these videos based on the logo of the application that created the Video.

Solutions Overview

arch.png<img width="834" alt="image" src="https://user-images.githubusercontent.com/117374837/202127411-857697bb-dc9c-466c-9ecb-378e0a8988e1.png">


The Solution workflow contains the following steps.

Part-1 ContentModeration Pipeline

    When any short video ( Maximum 10 MB in this case) gets uploaded into the S3 bucket, the lambda function calls the StartContentModeration API call on the Video.
    Once the StartContentModeration is invoked by the Lambda function, a JobId will be created and that is being pushed onto the Simple Notification Service. The Amazon SNS then triggers the next Lambda function that invokes the GetContentModeration API once the Job has been completed.
    If any Moderation Labels are detected the the video will be copied to a Destination bucket that will contain all the S3 buckets with Moderated contents

Part2- Custom model to Identify the plagiarism.

    The first Lambda function that invokes StartContentModeration API also contains the code to create an Elemental media Convert Job that converts the video into frames and and saves the first frame to an Intermediate S3 bucket that can be passed through Custom model project that is running on Amazon Rekognition.
    The elemental Media Convert job then converts the videos into frames and the First frame is analyzed against the Custom Model to Detect Labels.
    There is a Custom Model that is running in the AWS Rekognition, that is trained to detect the Logo of Mojo and Tiktok.
    In case any trained logos are detected it will then be moved to a second Destination bucket.

Prerequisites

For this walkthrough, you should have the following prerequisites:

    An AWS account
    An AWS Identity and Access Management (IAM) user with access to the following services and to follow the solution presented in this blog post, you should be familiar with the following AWS services and features:
    
    1. [Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
    2. AWS Lambda
    3. Amazon rekognition
    4. Amazon SNS
    5. Amazon Dynamodb
    6. AWS Cloudwatch
    7. AWS Cloudtrail
    8. AWS IAM

