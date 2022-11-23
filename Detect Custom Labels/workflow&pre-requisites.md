### **Part2 - Custom Modelling - Plagiraism checker**

In the "Start Content Moderation" section, a transcoding job is initiated to convert the Video into frames. The video will be saved onto an intermediate bucket with mp4 extension added to its name and also the first frame of the video will be saved as .0000000.jpg. This image is passed to the Custom Rekognition model for Label detection. (Here only first frame is considered as the Platform logo will be present on all the frames of the video).

In this section, we query the custom model using [DetectCustomLabels](https://docs.aws.amazon.com/rekognition/latest/APIReference/API_DetectCustomLabels.html) API call to detect plagiarism.  The API call takes the Rekognition takes the custom model version that you want to use and the input image as the required parameters.

Given below is the sample output of this Lambda function when the uploaded video contains a sharechat logo in its first frame

```
{
	'CustomLabels': [{
		'Name': 'sharechat',
		'Confidence': 92.1469955444336,
		'Geometry': {
			'BoundingBox': {
				'Width': 0.06157999858260155,
				'Height': 0.06356000155210495,
				'Left': 0.15749000012874603,
				'Top': 0.05685000121593475
			}
		}
	}],
	'ResponseMetadata': {
		'RequestId': '88c29f8a-5365-4428-a555-35265dacae0a',
		'HTTPStatusCode': 200,
		'HTTPHeaders': {
			'x-amzn-requestid': '88c29f8a-5365-4428-a555-35265dacae0a',
			'content-type': 'application/x-amz-json-1.1',
			'content-length': '208',
			'date': 'Sat, 18 Jun 2022 13:09:19 GMT'
		},
		'RetryAttempts': 0
	}
}
``` 

Based on the detected labels and the plagiarism check, the video files are stored in the relevant buckets.
