import boto3

def get_queues_message_totals(queues: list):
    """
    This function gets the total number of messages in each SQS queue. 
    """

    """
    :param queues: List of SQS queue URLs.
    :return: Dictionary with queue URLs as keys and message counts as values.
    """
    sqs = boto3.client('sqs')
    totals = {}

    for queue_url in queues:
        try:
            response = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            totals[queue_url] = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
        except Exception as e:
            print(f"Error getting message count for {queue_url}: {e}")
            totals[queue_url] = None

    return totals

if __name__ == "__main__":
    # queue urls to check for message totals
    queues = [
        "https://sqs.us-east-1.amazonaws.com/891612543788/green-queue",
        "https://sqs.us-east-1.amazonaws.com/891612543788/green-queue-dlq",
        "https://sqs.us-east-1.amazonaws.com/891612543788/red-queue",
        "https://sqs.us-east-1.amazonaws.com/891612543788/red-queue-dlq"
    ]
    # get message totals for the queues
    totals = get_queues_message_totals(queues)
    print(totals)