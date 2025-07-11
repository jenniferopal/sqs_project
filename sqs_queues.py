import sys
import boto3
import json

def get_queues_message_totals(queues: list) -> dict:
    """
    This function takes the list of full SQS queue URLs and returns them into a dictionary with the queue name and number of message in each queue. 
    """

    sqs = boto3.client('sqs')
    totals = {}
    processed_queues = set() # added to track processed URLs to avoid dupes

    for queue_url in queues:
        try:
            if queue_url.startswith('https://'):
                queue_identifier = queue_url.strip()  # Extract the queue identifier from the URL
            else: 
                print(f"Error: Please provide a valid SQS queue URL: {queue_url}", file=sys.stderr) # logs the error to stderr
                # takes the queue url and extract the end of the queue 
                queue_name = queue_url
                totals[queue_name] = None
                continue
            
            # this step will be skipped if processed already
            if queue_identifier in processed_queues:
                continue
            processed_queues.add(queue_identifier)  # this'll mark the queue as processed
            
            # extract queue name from url
            queue_name = queue_identifier.split('/')[-1]

            # gets the message count
            response = sqs.get_queue_attributes(
                QueueUrl=queue_url, 
                AttributeNames=['ApproximateNumberOfMessages']
            )

            # stores the message count in the totals dictionary
            totals[queue_name] = int(response['Attributes'].get('ApproximateNumberOfMessages', 0))
        
            #check for dead letter queue
            dlq_url = get_dlq_url_from_queue(sqs, queue_url)
            if dlq_url and dlq_url not in processed_queues:
                processed_queues.add(dlq_url)
                dlq_name = dlq_url.split('/')[-1]  # Extract the DLQ name from the URL

                try:
                    dlq_response = sqs.get_queue_attributes(
                        QueueUrl=dlq_url, 
                        AttributeNames=['ApproximateNumberOfMessages']
                    )
                    totals[dlq_name] = int(dlq_response['Attributes'].get('ApproximateNumberOfMessages', 0))
                except Exception as dlq_error:
                    print(f"Error getting DLQ message count for {dlq_url}: {dlq_error}", file=sys.stderr)
                    totals[dlq_name] = None

        except Exception as e:
            print(f"Error getting message count for {queue_url}: {e}", file=sys.stderr)  # logs the error to stderr
            # uses the identifier as key if the queue can't be extracted
            queue_name = queue_url.split('/')[-1]  if '/' in queue_identifier else queue_identifier 
            totals[queue_name] = None

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

# chosen to define the main function to allow for future expansion or command-line interface
def main():
    if len(sys.argv) < 2:
        print("Usage: python sqs_queues.py <queue_url1> <queue_url2> ...", file=sys.stderr)
        sys.exit(1)

    queue_urls = sys.argv[1:]
    totals = get_queues_message_totals(queue_urls)

    for queue_name, message_count in totals.items():
        print(f"{queue_name}: {message_count} messages")

if __name__ == "__main__":
    main()