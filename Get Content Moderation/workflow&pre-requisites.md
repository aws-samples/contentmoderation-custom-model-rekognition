## **Workflow**

#### **Pre-requisities :**

Post the completion of the content moderation job from section "Start Content Moderation", Rekognition posts the completion status of the job to the SNS topic which is inturn subscribed by this Lambda function. This section is responsible for retrieving the analysis results of the Video analysis started by StartContentModeration job in the previous section.

Sample output of the function when the video contains the Moderation Labels and when a moderation label is detected the Video is moved to a different Destination bucket which is further passed for a human review.

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
