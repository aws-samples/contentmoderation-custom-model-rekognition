
README.md

**A Video Content Moderation Technique with a Custom Model to identify the plagiarism in short Video Applications**

When the short Video Applications cross millions of users, it becomes difficult to monitor, assess, and filter uploaded videos based on a predetermined set of rules. Content moderation technique is inevitable as it helps to maintain and enforce community guidelines.This Solution provides a Content Moderation pipeline that will ensure that their end-users are not exposed to potentially inappropriate or offensive material, such as nudity, violence, drug use, adult products, or disturbing images. Also it contains a Custom model to identify Plagiarism which means it helps you to identify any video being uploaded on to our application which is created using another platform. We tag these videos based on the logo of the application that created the Video.

**Solutions Overview**

arch.png<img width="834" alt="image" src="https://user-images.githubusercontent.com/117374837/202127411-857697bb-dc9c-466c-9ecb-378e0a8988e1.png">


The Solution workflow contains the following steps.

**Part-1 ContentModeration Pipeline**

    When any short video ( Maximum 10 MB in this case) gets uploaded into the S3 bucket, the lambda function calls the StartContentModeration API call on the Video.
    Once the StartContentModeration is invoked by the Lambda function, a JobId will be created and that is being pushed onto the Simple Notification Service. The Amazon SNS then triggers the next Lambda function that invokes the GetContentModeration API once the Job has been completed.
    If any Moderation Labels are detected the the video will be copied to a Destination bucket that will contain all the S3 buckets with Moderated contents

**Part2- Custom model to Identify the plagiarism.**

    The first Lambda function that invokes StartContentModeration API also contains the code to create an Elemental media Convert Job that converts the video into frames and and saves the first frame to an Intermediate S3 bucket that can be passed through Custom model project that is running on Amazon Rekognition.
    The elemental Media Convert job then converts the videos into frames and the First frame is analyzed against the Custom Model to Detect Labels.
    There is a Custom Model that is running in the AWS Rekognition, that is trained to detect the Logo of Mojo and Tiktok.
    In case any trained logos are detected it will then be moved to a second Destination bucket.

**Prerequisites**

For this walkthrough, you should have the following prerequisites:

<a href="https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html">An AWS account</a> <br>

An AWS Identity and Access Management (IAM) user with access to the following services and to follow the solution presented in this blog post, you should be familiar with the following AWS services and features:
    
<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html">Amazon S3</a><br>
<a href="https://docs.aws.amazon.com/toolkit-for-eclipse/v1/user-guide/lambda-tutorial.html">AWS Lambda</a><br>
<a href="https://docs.aws.amazon.com/managedservices/latest/userguide/rekognition.html">Amazon rekognition </a><br>
<a href="https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/sns-examples.html">Amazon SNS </a><br>
<a href="https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html">Amazon Dynamodb</a><br>
<a href="https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_architecture.html">AWS Cloudwatch</a><br> 
<a href="https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html">AWS Cloudtrail </a><br>
<a href="https://docs.aws.amazon.com/iam/index.html">AWS IAM</a><br>


**Creating Custom Modelling for Plagiarism Detection on Amazon Rekognition**

I have explained the steps below to create a Custom Rekognition project via AWS Console, Creating  Dataset by uploading the images from the local machine , Labelling it via bounding boxes from the console and Starting the model.

**Creating a custom Model project in Amazon Rekognition console**

1.	Login to AWS Console and search for Amazon Rekognition. Go to Use Custom Labels under Custom Labels.

2.	Click on "Projects" on the left 

 
a.png![image](https://user-images.githubusercontent.com/117374837/202370197-0986f523-4954-4b82-903e-e668473ae25b.png)
 

3.	Click on Create Project
 

b.png![image](https://user-images.githubusercontent.com/117374837/202370272-50e12d1f-9ed9-4d0e-b0ef-9cf91fcc86d8.png)


4.	Give a name to the Project and click on  Create Project 


c.png![image](https://user-images.githubusercontent.com/117374837/202370443-43717b47-1670-4423-be90-7103e2aa8944.png)



**Creating a Dataset and Labelling it**


1.	Click on the Name of the Project and click on “Create Dataset”
        

d.png![image](https://user-images.githubusercontent.com/117374837/202371107-2a6c5b77-42f9-4b4f-b91a-4cdaa1349ab9.png)

         
2.	Select the Option “Start with a Single Dataset” for this Demo and Choose the Option “Upload Images from your Computer”
  
 

e.png![image](https://user-images.githubusercontent.com/117374837/202376616-e62afeb2-7cb2-4147-bd21-dc3077e80756.png)


3.	Download the images given in the folder “images” which includes the images of tiktok , sharechat  and Moj logos collected from Internet to your local machine and then upload these images using Add Images.

 
f.png![image](https://user-images.githubusercontent.com/117374837/202376686-3210051b-c58f-40e9-bc0f-c96c75ee87fa.png)
 

4.	You will get a window like this and click on Choose Files and after selecting the files, Click Upload Images.



g.png![image](https://user-images.githubusercontent.com/117374837/202376907-f6a58374-276c-4558-b0db-81c0045c9264.png)


   **Labelling the Images**

1.	Click on Start Labelling


h.png![image](https://user-images.githubusercontent.com/117374837/202376963-26a982dc-cf5b-4a4e-bb5f-ddd4fdf23a88.png)


2.	Click on Add Labels and add labels with Names Tiktok, Mojo and sharechat


i.png![image](https://user-images.githubusercontent.com/117374837/202376998-137f2603-6fd1-4c49-b885-5d7ae87bb265.png)


3.	Select the Images and Click on Draw Bounding boxes. 
  

j.png![image](https://user-images.githubusercontent.com/117374837/202377068-2a98a926-338b-4baa-b88c-15c5997ef85c.png)


4.	After drawing bounding boxes on all the images, click Done.

**Training the Custom Model**

1. Now we will need to train our model and click on Tran model which is the third option in the screenshot. It will take some time ( 30 minutes to 24 hours ) based on the number of images.



k.png![image](https://user-images.githubusercontent.com/117374837/202377132-9bdc7c8f-55f4-43bb-b219-47fa65c34b8b.png)


2.	Now  click on “Check Metrics under the “Evaluating your model to check the performance.


l.png![image](https://user-images.githubusercontent.com/117374837/202377201-3f6ad53a-78ae-4674-8c8a-9f1b56c69039.png)

Refer: https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/im-metrics-use.html
 
3. Now go to “Use Model” and Click on Start Model. You can choose the number of Inference units and as the number of inference unit increases, the throughout also increases.


m.png![image](https://user-images.githubusercontent.com/117374837/202377338-a1545405-71bf-4ee0-b1d6-2e0425f8fe9b.png)
 

**Part-1 Content Moderation – Workflow and Outputs** 

1.The First Lambda function Lambda1 invokes StartContentModeration API and based on the size of the video it take some time for the Content Moderation job to finish. Once it is finished it generates a JobID and that is passed to Simple Notification Service to Trigger  the next Lambda function that invokes the GetContentModeration API. Lambda1  itself has the function to create an Elemental Media convert job to convert the video into frames that will be required to run a custom Rekognition model. 

 
Please find the JobID output from the Lambda function


{
    "JobId": "3ffd9326c88e8194b35cf102644a2b8fb587684a2617820ad0fe593ac75ae525",
    "ResponseMetadata": {
        "RequestId": "7029e5f9-24f7-4b99-9ac3-4e44806af6da",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "7029e5f9-24f7-4b99-9ac3-4e44806af6da",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "76",
            "date": "Thu, 22 Sep 2022 09:02:57 GMT"
        },
        "RetryAttempts": 0
    }
}


2. As mentioned, Once the JobID is generated the SNS triggers the second Lambda function  Lambda2 and it invokes the GetContentModeration API. I have quoted the sample output of the function when the video contains the Moderation Labels and when a moderation label is detected the Video is moved to a different Destination bucket which is further passed for a human review. 

[{
    "Timestamp": 66,
    "ModerationLabel": {
        "Confidence": 98.96820831298828,
        "Name": "Barechested Male",
        "ParentName": "Suggestive"
    }
}, {
    "Timestamp": 66,
    "ModerationLabel": {
        "Confidence": 98.96820831298828,
        "Name": "Suggestive",
        "ParentName": ""
    }
}, {
    "Timestamp": 566,
    "ModerationLabel": {
        "Confidence": 97.36837768554688,
        "Name": "Barechested Male",
        "ParentName": "Suggestive"
    }
}, {
    "Timestamp": 566,
    "ModerationLabel": {
        "Confidence": 97.36837768554688,
        "Name": "Suggestive",
        "ParentName": ""
    }
]

**Part2 - Custom Modelling **

1.	Lambda1 will also convert the Video into frames. The video will be saved onto an intermediate bucket with mp4 extension added to its name and also the first frame of the video will be saved as <videoname>.0000000.jpg. This image is passed to the Custom Rekognition model for Label detection. (Here only first frame is considered as the Platform logo will be present on all the frames of the video)


2.	Whenever an input frame comes to the intermediate bucket another Lambda function , Lambda3  is triggered and it will invoke DetectCustomLabels API call. 


Given below is the output of this Lambda function

{'CustomLabels': [{'Name': 'sharechat', 'Confidence': 92.1469955444336, 'Geometry': {'BoundingBox': {'Width': 0.06157999858260155, 'Height': 0.06356000155210495, 'Left': 0.15749000012874603, 'Top': 0.05685000121593475}}}], 'ResponseMetadata': {'RequestId': '88c29f8a-5365-4428-a555-35265dacae0a', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': '88c29f8a-5365-4428-a555-35265dacae0a', 'content-type': 'application/x-amz-json-1.1', 'content-length': '208', 'date': 'Sat, 18 Jun 2022 13:09:19 GMT'}, 'RetryAttempts': 0}}

So if any of the trained logos (Moj, sharechat or tiktok )  detected the video is moved to another Bucket






