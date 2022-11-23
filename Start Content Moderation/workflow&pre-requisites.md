**Workflow and Outputs**

1.This Lambda function invokes StartContentModeration API and based on the size of the video it take some time for the Content Moderation job to finish. Once it is finished it generates a JobID and that is passed to Simple Notification Service to Trigger the next Lambda function that invokes the GetContentModeration API. It also has the function to create an Elemental Media convert job to convert the video into frames that will be required to run a custom Rekognition model.

Please find the JobID output from the Lambda function which is passed to SNS.

```json
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
```

  As mentioned, Once the JobID is generated the SNS triggers the second Lambda function Lambda2 and it invokes the GetContentModeration API. I have quoted the sample output of the function when the video contains the Moderation Labels and when a moderation label is detected the Video is moved to a different Destination bucket which is further passed for a human review.

```
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
	}]
```

