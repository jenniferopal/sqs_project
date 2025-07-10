import sys
import boto3

def get_queues_message_totals(queues: list) -> dict:
    """
    This function takes the list of full SQS queue URLs and returns them into a dictionary with the queue name and number of message in each queue. 
    """

    sqs = boto3.client('sqs')
    totals = {}

    for queue_url in queues:
        try:
            # takes the queue url and extract the end of the queue 
            queue_name = queue_url.strip().split('/')[-1] # Extract the queue name from the URL
            response = sqs.get_queue_attributes(
                QueueUrl=queue_url,
                AttributeNames=['ApproximateNumberOfMessages']
            )
            
            totals[queue_name] = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
        except Exception as e:
            print(f"Error getting message count for {queue_url}: {e}", file=sys.stderr) #logs the error to stderr
            totals[queue_name] = None

    return totals

if __name__ == "__main__":

    queues = [
        "https://sqs.us-east-1urls.amazonaws.com/891612543788/green-queue",
        "https://sqs.us-east-1.amazonaws.com/891612543788/red-queue"
    ]

    # message totals for each queue
    message_totals = get_queues_message_totals(queues)

    # this loops through the dictionary to print the results
    for queue_name, count in message_totals.items():
        print(f"Queue: {queue_name}, Messages: {count}")
    queue_name = {queue.split('/')[-1]: queue for queue in queues}  