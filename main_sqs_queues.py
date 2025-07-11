import sys
import json
import boto3

def get_queues_message_totals(queues: list):
    """
    This function takes the list of full SQS queue names and returns them into a dictionary with the queue name including their dead letter queue. 
    """
    sqs = boto3.client('sqs')
    totals = {}
    processed_queues = set()  # Track processed queue names to avoid duplicates

    for queue_id in queues:
        # Skip if we've already processed this queue
        if queue_id in processed_queues:
            continue
        processed_queues.add(queue_id)
        
        try:
            # Get the full queue URL from the queue name
            queue_url = get_queue_url_from_name(sqs, queue_id)
            if not queue_url:
                totals[queue_id] = None
                continue
            
            # Get message count for main queue
            try:
                response = sqs.get_queue_attributes(
                    QueueUrl=queue_url,
                    AttributeNames=['ApproximateNumberOfMessages']
                )
                totals[queue_id] = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
            except Exception as queue_error:
                print(f"Error getting message count for {queue_id}: {queue_error}", file=sys.stderr)
                totals[queue_id] = None
                continue
            
            # Check for dead letter queue
            dlq_url = get_dlq_url_from_queue(sqs, queue_url)
            if dlq_url:
                dlq_name = dlq_url.split('/')[-1]
                
                # Only process DLQ if we haven't already processed it
                if dlq_name not in processed_queues:
                    processed_queues.add(dlq_name)
                    try:
                        dlq_response = sqs.get_queue_attributes(
                            QueueUrl=dlq_url,
                            AttributeNames=['ApproximateNumberOfMessages']
                        )
                        totals[dlq_name] = int(dlq_response['Attributes'].get('ApproximateNumberOfMessages', 0))
                    except Exception as dlq_error:
                        print(f"Error getting DLQ message count for {dlq_name}: {dlq_error}", file=sys.stderr)
                        totals[dlq_name] = None
                    
        except Exception as e:
            print(f"Error processing queue {queue_id}: {e}", file=sys.stderr)
            totals[queue_id] = None

    return totals

def get_dlq_url_from_queue(sqs_client, queue_url: str):
    """
    Get the dead letter queue URL for a given queue by checking its RedrivePolicy.
    """
    try:
        response = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['RedrivePolicy']
        )
        
        redrive_policy = response['Attributes'].get('RedrivePolicy')
        if redrive_policy:
            # Parse the JSON to get the dead letter queue ARN
            policy = json.loads(redrive_policy)
            dlq_arn = policy.get('deadLetterTargetArn')
            
            if dlq_arn:
                # Convert ARN to queue URL
                # ARN format: arn:aws:sqs:region:account-id:queue-name
                arn_parts = dlq_arn.split(':')
                region = arn_parts[3]
                account_id = arn_parts[4]
                dlq_name = arn_parts[5]
                
                dlq_url = f"https://sqs.{region}.amazonaws.com/{account_id}/{dlq_name}"
                return dlq_url
                
    except Exception as e:
        print(f"Warning: Could not get DLQ for {queue_url}: {e}", file=sys.stderr)
    
    return None

def get_queue_url_from_name(sqs_client, queue_name: str):
    """
    Get the full queue URL from just the queue name.
    """
    try:
        response = sqs_client.get_queue_url(QueueName=queue_name)
        return response['QueueUrl']
    except Exception as e:
        print(f"Error getting URL for queue '{queue_name}': {e}", file=sys.stderr)
        return None

# chosen to define the main function to allow for future expansion or command-line interface    
def main():
    if len(sys.argv) < 2:
        print("Usage: python sqs_queues.py <queue-name-1> <queue-name-2> ...", file=sys.stderr)
        print("Example: python sqs_queues.py queue-1 queue-2 queue-3", file=sys.stderr)
        sys.exit(1)
    
    queue_names = sys.argv[1:]
    
    # Get message totals for all queues
    message_totals = get_queues_message_totals(queue_names)
    
    # Output results to stdout
    for queue_name, count in message_totals.items():
        if count is not None:
            print(f"Queue: {queue_name}, Messages: {count}")
        else:
            print(f"Queue: {queue_name}, Messages: ERROR")

if __name__ == "__main__":
    main()