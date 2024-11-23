import json, boto3
import pymysql

# Lambda
client = boto3.client('lambda', region_name='us-east-1')

# MySQL
host = 'mtcarsdb.c9qca4k6aw1y.us-east-1.rds.amazonaws.com'
user = "mtcarsUsername"
password = "mtcars123"
database = "MTCars"

# This handler is run every time the Lambda function is invoked
def lambda_handler(event, context):
    # Show the incoming event in the debug log
    print("Event received by Lambda function: " + json.dumps(event, indent=2))
    
    try:
        log = json.loads(event['body'])
        car = log.get('car')
    except (json.JSONDecodeError, KeyError) as e:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid car model or year.')
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
            # Insert a new record into the CarData table
            try:
                cursor.execute("SELECT MAX(id) FROM MTCars;")
                max_id = cursor.fetchone()[0]  # Fetch the maximum ID
                print(f"Max ID: {max_id}")
                
                cursor.execute(
                    "INSERT INTO MTCars (ID, NAME, MPG, CYL, DISP, HP, WT, QSEC, VS, AM, GEAR, ANO) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                    (
                        str(max_id + 1),
                        car['name'],
                        car['mpg'],
                        car['cyl'],
                        car['disp'],
                        car['hp'],
                        car['wt'],
                        car['qsec'],
                        car['vs'],
                        car['am'],
                        car['gear'],
                        car['ano']
                    )
                )
                connection.commit()
            except pymysql.MySQLError as e:
                print(f"Error inserting data: {e}")
                return {
                    'statusCode': 500,
                    'body': json.dumps("Insertion failed.")
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
        
        payload = json.dumps({
            "car_name": car['name'],
            "car_year": car['ano']
        })

        client.invoke(
            FunctionName='arn:aws:lambda:us-east-1:891377033678:function:check_waiting_users',
            InvocationType='Event', # Asynchronous
            Payload=payload
        )
    return {
        'statusCode': 200,
        'body': json.dumps('Function ran without errors.')
    }