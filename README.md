# SQS Module

A Terraform module that creates SQS queues with dead letter queues and IAM policies.

## Usage

```hcl
module "sqs_queues" {
  source = "./sqs-module"
  queue_names = ["processing-queue", "notification-queue"]
  create_roles = true
}
```

## Variables

- `queue_names` - List of queue names (default: `["queue-1", "queue-2", "queue-3"]`)
- `create_roles` - Create IAM roles (default: `true`)

## Outputs

- `queue_arns` - Map of queue ARNs
- `consume_policy_arn` - Consumer policy ARNs
- `write_policy_arn` - Producer policy ARNs
- `consumer_roles` - Consumer role ARNs (if created)
- `producer_roles` - Producer role ARNs (if created)

## SQS Monitoring Script

The `sqs_queues.py` script monitors message counts in your queues and automatically discovers their dead letter queues.

### Setup

1. Install boto3: `pip install boto3`
2. Configure AWS credentials
3. Obtain your full SQS queue URLs from the AWS Console

### Usage

**Command Line:**
```bash
python sqs_queues.py https://sqs.us-east-1.amazonaws.com/YOUR-ACCOUNT-ID/queue-1 https://sqs.us-east-1.amazonaws.com/YOUR-ACCOUNT-ID/queue-2
```

**Import in Python:**
```python
from sqs_queues import get_queues_message_totals

queues = [
    "https://sqs.us-east-1.amazonaws.com/YOUR-ACCOUNT-ID/processing-queue",
    "https://sqs.us-east-1.amazonaws.com/YOUR-ACCOUNT-ID/notification-queue"
]

totals = get_queues_message_totals(queues)
print(totals)
```

### Output

```
Queue: processing-queue, Messages: 42
Queue: processing-queue-dlq, Messages: 2
Queue: notification-queue, Messages: 0
Queue: notification-queue-dlq, Messages: 0
```

### Features

- **Automatic DLQ Discovery**: The script automatically finds and includes dead letter queue message counts
- **Error Handling**: Failed queue operations are logged to stderr and return `None`
- **Flexible Input**: Accepts full SQS queue URLs
- **Dual Interface**: Works both as a command-line tool and importable Python module

### Notes

- Dead letter queue names shouldn't be passed to the function - they're discovered automatically
- The script requires full queue URLs, not just queue names
- Any errors accessing queues are printed to stderr whilst continuing to process other queues