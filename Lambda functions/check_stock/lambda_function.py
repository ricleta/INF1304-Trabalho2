import json, boto3
import pymysql

# MySQL
host = 'mtcarsdb.c9qca4k6aw1y.us-east-1.rds.amazonaws.com'
user = "mtcarsUsername"
password = "mtcars123"
database = "MTCars"

# This handler is run every time the Lambda function is invoked
def lambda_handler(event, context):
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))
    
    log = json.loads(event['body'])
    # Parse the event body to get the parameters
    car_model = log.get('car_model')
    car_year = log.get('car_year')
    email = log.get('email')

    if not car_model or not car_year or not email:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Invalid car model or year or email.',
                'car_model': car_model,
                'car_year': car_year,
                'email': email
            })
        }

    try:
        # Connect to RDS MySQL
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        with connection.cursor() as cursor:
            # Query for a specific model of car (Use parameterized query to prevent SQL injection)
            cursor.execute("SELECT * FROM MTCars WHERE NAME = %s AND ANO = %s", (car_model, car_year))
            result = cursor.fetchone()
            
            if result:
                # Construct message to be sent
                message = f"A {car_model} {car_year} is available in the inventory. Hurry up and get it!"
                
                # Connect to SNS
                sns = boto3.client('sns')
                alertTopic = 'CarAvailable'
                try:
                    snsTopicArn = [t['TopicArn'] for t in sns.list_topics()['Topics'] if t['TopicArn'].lower().endswith(':' + alertTopic.lower())][0]
                    
                    # Send message to SNS
                    sns.publish(
                        TopicArn=snsTopicArn,
                        Message=message,
                        Subject='Car Availability Alert!',
                        MessageStructure='raw',
                        MessageAttributes={
                            'recipient': {
                                'DataType': 'String',
                                'StringValue': str(email)
                            }
                        }
                    )
                        
                except boto3.exceptions.Boto3Error as e:
                    print(f"Error sending SNS message: {e}")
                    return {
                        'statusCode': 500,
                        'body': json.dumps(f"Error sending SNS message: {str(e)}")
                    }
            else:
                message = f"Sorry, we don't have a {car_model} {car_year} in our inventory."
                return {
                    'statusCode': 404,
                    'body': json.dumps(message)
                }
    
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"MySQL connection error: {str(e)}")
        }
    except KeyError as e:
        print(f"Key error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"Missing parameter: {str(e)}")
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error: {str(e)}")
        }
    finally:
        connection.close()

    return {
        'statusCode': 200,
        'body': json.dumps('Function ran without errors.')
    }