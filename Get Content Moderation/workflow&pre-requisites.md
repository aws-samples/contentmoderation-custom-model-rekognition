**Workflow and Outputs**

Once the JobID is generated by the Start Content Moderation Lambda function, the SNS triggers this Lambda function and it invokes the GetContentModeration API. I have quoted the sample output of the function when the video contains the Moderation Labels and when a moderation label is detected the Video is moved to a different Destination bucket which is further passed for a human review.

[{ "Timestamp": 66, "ModerationLabel": { "Confidence": 98.96820831298828, "Name": "Barechested Male", "ParentName": "Suggestive" } }, { "Timestamp": 66, "ModerationLabel": { "Confidence": 98.96820831298828, "Name": "Suggestive", "ParentName": "" } }, { "Timestamp": 566, "ModerationLabel": { "Confidence": 97.36837768554688, "Name": "Barechested Male", "ParentName": "Suggestive" } }, { "Timestamp": 566, "ModerationLabel": { "Confidence": 97.36837768554688, "Name": "Suggestive", "ParentName": "" } ]