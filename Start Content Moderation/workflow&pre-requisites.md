**Workflow and Outputs**

This section accomodates 2 parts :
1. Start an asynchronous job to detect inappropriate, unwanted, or offensive content in a stored video using [StartContentModeration](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StartContentModeration.html) API.
2. Convert video into frames using a Transcoding job using [CreateJob](https://docs.aws.amazon.com/mediaconvert/latest/apireference/jobs.html#jobspost) API call

Workflow :

1. This Lambda function invokes [StartContentModeration](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_StartContentModeration.html) API which starts asynchronous detection of inappropriate, unwanted, or offensive content in a stored video. Once the job is successfully submitted, a JobID is returned back to the user. In order to track the completion status, we use a notification channel using Simple Notification Service to Trigger the next Lambda function to execute the [GetContentModeration](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_GetContentModeration.html) API to retrieve the results.

Sample output of StartContentModeration API :

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

2. Cre
