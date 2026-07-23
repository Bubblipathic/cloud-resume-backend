import json
import boto3
from botocore.exceptions import ClientError

# Initialize the SES client
ses = boto3.client('ses', region_name='ap-southeast-1') # Use your specific region

def lambda_handler(event, context):
    try:
        # 1. Parse the incoming JSON from the frontend
        body = json.loads(event['body'])
        sender_name = body.get('name')
        sender_email = body.get('email')
        subject = body.get('subject')
        message = body.get('message')

        # 2. Format the email content
        # Send FROM your verified custom domain (This uses your DKIM/SPF records!)
        from_email = "noreply@jaymart-reario.abrdns.com"
        # We put the visitor's email in the Reply-To field so you can hit "Reply" in Gmail.
        my_email = "jaymartreario@gmail.com" # Replace with your verified SES email
        
        email_body = f"""
        New Contact Form Submission from your Cloud Resume!
        
        Name: {sender_name}
        Email: {sender_email}
        Subject: {subject}
        
        Message:
        {message}
        """

        # 3. Send the email via SES
        response = ses.send_email(
            Source=from_email,
            Destination={
                'ToAddresses': [my_email]
            },
            Message={
                'Subject': {'Data': f"Portfolio Contact: {subject}"},
                'Body': {'Text': {'Data': email_body}}
            },
            ReplyToAddresses=[sender_email] if sender_email else []
        )

        # 4. Return success to the frontend
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully!'})
        }

    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        # Catch the specific 200-limit error
        if error_code == 'LimitExceededException' or error_code == 'Throttling':
            return {
                'statusCode': 429,
                'body': json.dumps({'error': 'Daily message limit reached. Please try again tomorrow!'})
            }
            
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to send email via SES'})
        }

    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Bad Request'})
        }