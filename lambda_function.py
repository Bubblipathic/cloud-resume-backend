_import json
import boto3

# Instantiate 
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('cloud-resume-visitor-count')

def lambda_handler(event, context):
    # 1. Retrieve the current item from DynamoDB
    response = table.get_item(Key={'id': 'visitor_count'})
    # 2. Extract the current count number
    current_count = response['Item']['number']
    # 3. Add 1 to the count
    new_count = current_count + 1
    # 4. Save the updated count back to the database
    table.put_item(Item={
        'id': 'visitor_count',
        'number': new_count
    })

    return {
        'statusCode': 200,
        # This CORS header is crucial so your HTML page is allowed to read this data
        'headers': {
            'Access-Control-Allow-Origin': '*' 
        },
        'body': json.dumps({'number': int(new_count)})
    }
    
