import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource("dynamodb", region_name="ap-south-1")
table = dynamodb.Table("student-use-history")

def save_interaction(user_id: str, question: str, response: str):
    """
    Save user interaction in DynamoDB
    """
    table.put_item(
        Item={
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "question": question,
            "response": response,
            "timestamp": str(datetime.utcnow())
        }
    )
