
README.md

**A Video Content Moderation Technique with a Custom Model to identify the plagiarism in short Video Applications**

When the short Video Applications cross millions of users, it becomes difficult to monitor, assess, and filter uploaded videos based on a predetermined set of rules. Content moderation technique is inevitable as it helps to maintain and enforce community guidelines. This Solution provides a Content Moderation pipeline that will ensure that their end-users are not exposed to potentially inappropriate or offensive material, such as nudity, violence, drug use, adult products, or disturbing images. Also it contains an Amazon Rekognition Custom model to identify Plagiarism which means it helps you to identify any video being uploaded on to our application which is created using another platform. We tag these videos based on the logo of the application that created the Video. We have considered the applications Moj,Sharechat and Tiktok in this Demo.

**Solutions Overview**

arch.png<img width="834" alt="image" src="https://user-images.githubusercontent.com/117374837/202127411-857697bb-dc9c-466c-9ecb-378e0a8988e1.png">


The Solution workflow contains the following steps.

**Part-1 ContentModeration Pipeline**

    When any short video ( Maximum 10 MB in this case) gets uploaded into the S3 bucket, the lambda function calls the StartContentModeration API call on the Video.
    Once the StartContentModeration is invoked by the Lambda function, a JobId is returned by the service once the asynchronous job is submitted. A notification channel is used to track the completion status of the job. The Amazon SNS topic (notification channel) then triggers the next Lambda function that invokes the GetContentModeration API once the Job has been completed.
    If any Moderation Labels are detected the the video will be copied to a Destination bucket that will contain all the S3 buckets with Moderated contents

**Part2- Custom model to Identify the plagiarism.**

    The first Lambda function that invokes StartContentModeration API also creates an Elemental media Convert Job that converts the video into frames and and saves the first frame to an Intermediate S3 bucket that can be passed through Custom model project that is running on Amazon Rekognition.
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

Below are the steps to create a Custom Rekognition project via AWS Console, Creating  Dataset by uploading the images from the local machine , Labelling it via bounding boxes from the console and Starting the model.

**Creating a custom Model project in Amazon Rekognition console**

1.	Login to AWS Console and search for Amazon Rekognition. Go to Use Custom Labels under Custom Labels.

2.	Click on "Projects" on the left 

 
![image](https://user-images.githubusercontent.com/117374837/202370197-0986f523-4954-4b82-903e-e668473ae25b.png)
 

3.	Click on Create Project
 

![image](https://user-images.githubusercontent.com/117374837/202370272-50e12d1f-9ed9-4d0e-b0ef-9cf91fcc86d8.png)


4.	Give a name to the Project and click on Create Project 


![image](https://user-images.githubusercontent.com/117374837/202370443-43717b47-1670-4423-be90-7103e2aa8944.png)



**Creating a Dataset and Labelling it**


1.	Click on the Name of the Project and click on “Create Dataset”
        

![image](https://user-images.githubusercontent.com/117374837/202371107-2a6c5b77-42f9-4b4f-b91a-4cdaa1349ab9.png)

         
2.	Select the Option “Start with a Single Dataset” for this Demo and Choose the Option “Upload Images from your Computer”
  
 

![image](https://user-images.githubusercontent.com/117374837/202376616-e62afeb2-7cb2-4147-bd21-dc3077e80756.png)


3.	Download the images given in the folder “images” which includes the images of tiktok , sharechat  and Moj logos collected from Internet to your local machine and then upload these images using Add Images.

 
![image](https://user-images.githubusercontent.com/117374837/202376686-3210051b-c58f-40e9-bc0f-c96c75ee87fa.png)
 

4.	Cick on Choose Files and upon selecting the files, Click Upload Images.



![image](https://user-images.githubusercontent.com/117374837/202376907-f6a58374-276c-4558-b0db-81c0045c9264.png)


   **Labelling the Images**

1.	Click on Start Labelling


![image](https://user-images.githubusercontent.com/117374837/202376963-26a982dc-cf5b-4a4e-bb5f-ddd4fdf23a88.png)


2.	Click on Add Labels and add labels with Names Tiktok, Mojo and sharechat


![image](https://user-images.githubusercontent.com/117374837/202376998-137f2603-6fd1-4c49-b885-5d7ae87bb265.png)


3.	Select the Images and Click on Draw Bounding boxes. 
  

![image](https://user-images.githubusercontent.com/117374837/202377068-2a98a926-338b-4baa-b88c-15c5997ef85c.png)


4.	After drawing bounding boxes and labelling the images, click Done.

**Training the Custom Model**

1. Now we will need to train our model and click on Tran model which is the third option in the screenshot. This can take 30 minutes to 24 hours based on the number of images.



![image](https://user-images.githubusercontent.com/117374837/202377132-9bdc7c8f-55f4-43bb-b219-47fa65c34b8b.png)


2. Use “Check Metrics" under the “Evaluating your model to inspect the modelperformance.


![image](https://user-images.githubusercontent.com/117374837/202377201-3f6ad53a-78ae-4674-8c8a-9f1b56c69039.png)

Refer: https://docs.aws.amazon.com/rekognition/latest/customlabels-dg/im-metrics-use.html
 
3. Now go to “Use Model” and Click on Start Model. You can choose the number of Inference units which determines the throughput of the model


![image](https://user-images.githubusercontent.com/117374837/202377338-a1545405-71bf-4ee0-b1d6-2e0425f8fe9b.png)
 
