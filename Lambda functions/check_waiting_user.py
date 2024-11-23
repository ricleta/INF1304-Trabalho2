import json, boto3
from boto3.dynamodb.conditions import Attr

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')

# Connect to the DynamoDB tables
userTable = dynamodb.Table('waiting_clients')

def lambda_handler(event, context):
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))

    print("Antes do try")
        
    car_model = event['car_name']
    car_year = event['car_year']

    if not car_model or not car_year:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid car model or year.')
        }

    print(f"Passei o try, car_model = {car_model}, car_year = {car_year}")
    
    # Look for any user that might be waiting for this car
    # response = userTable.scan(
    #     FilterExpression=Attr('car_name').eq(car_model) & Attr('car_year').eq(car_year)
    # )

    response = userTable.scan()
    print(f"{response['Count']} users are waiting for the car {car_model} {car_year}.")

    if response['Count'] > 0:
        sns = boto3.client('sns')
        alertTopic = 'CarAvailable'
        snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]

        # Creates a set with the emails of the interested users
        interested_users = set()
        for item in response['Items']:
            print(f"item = {item}")
            print(f"item['car_name'] = {item['car_name']}")
            print(f"item['car_year'] = {item['car_year']}")
            if str(item['car_name']) == str(car_model) and str(item['car_year']) == str(car_year):
                print(f"Adding {item['email']} to the interested users.")
                interested_users.add(item['email'])
        # interested_users = set(item['email'] for item in response['Items'])


        # Send a message to the interested users
        for email in interested_users:
            sns.publish(
                TopicArn=snsTopicArn,
                Message=f"The car {car_model} {car_year} is now available!",
                Subject="Car Available",
                MessageAttributes={
                    'recipient': {
                        'DataType': 'String',
                        'StringValue': str(email)
                    }
                }
            )

            userTable.delete_item(
                Key={
                    'email': email,
                    'sort_key': f"{car_model},{car_year}"
                }
            )
            
            print(f"Email sent to {email}.")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

    