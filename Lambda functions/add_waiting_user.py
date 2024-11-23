import json, boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
inventoryTable = dynamodb.Table('waiting_clients')

# This handler is run every time the Lambda function is invoked
def lambda_handler(event, context):
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))
    
    if 'body' in event:
        # Parse the event body to get the parameters
        try:
            log = json.loads(event['body'])
        except json.JSONDecodeError:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'message': 'Invalid JSON in request body.'
                })
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Request body is missing.'
            })
        }

    email = log.get('email')
    desired_car_name = log.get('car_name')
    desired_car_year = log.get('car_year') 
    sort_key = f"{desired_car_name},{desired_car_year}"
    print(email, desired_car_name, desired_car_year)
        
    try:
        # Insert Store, Item and Count into the Inventory table
        inventoryTable.put_item(Item={
            'email': email,
            'sort_key': sort_key,
            'car_name': desired_car_name,
            'car_year': desired_car_year})
        print("inserted")
    except Exception as e:
        print(e)
        print("Unable to insert data into DynamoDB table".format(e))
        raise(e)
        
    # Finished!
    return {
        'statusCode': 200,
        'body': f"Added {email} to the waiting list for {desired_car_name} {desired_car_year} successfully."
    }
