import json, boto3

# Connect to S3 and DynamoDB
s3 = boto3.resource('s3')
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
inventoryTable = dynamodb.Table('Inventory')

# This handler is run every time the Lambda function is invoked
def lambda_handler(event, context):
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))
    
    try:
        log = json.loads(event['body'])
    except (KeyError, TypeError, json.JSONDecodeError):
        return {
            "statusCode" : 400,
            "body": json.dumps({"message": "No json body or bad request"})
        }
        
    # Read each row in the file
    rowCount = 0
    for row in log:
        rowCount += 1
        store = row.get('store')
        item = row.get('item')
        count = row.get('count')
        
        # Show the row in the debug log
        print(store, item, count)
        
        try:
            # Insert Store, Item and Count into the Inventory table
            inventoryTable.put_item(Item={
                'Store': store,
                'Item': item,
                'Count': int(count)})
        except Exception as e:
            print(e)
            print("Unable to insert data into DynamoDB table".format(e))
            raise(e)
            
    # Finished!
    return {
        'statusCode': 200,
        'body': f"{rowCount} counts inserted"
    }
