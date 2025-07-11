# SQS Module

A Terraform module that creates SQS queues with dead letter queues and IAM policies.

## Usage

```hcl
module "sqs_queues" {
  source = "./sqs-module"
  queue_names = ["queue-1", "queue-2"]
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
3. Obtain your SQS queue names from the AWS Console

### Usage

**Command Line:**
```bash
python sqs_queues.py queue-1 queue-2 queue-3
```

**Import in Python:**
```python
from sqs_queues import get_queues_message_totals

queue_names = ["queue-1", "queue-2"]
totals = get_queues_message_totals(queue_names)
print(totals)
```

### Output

```
queue-1: 42 messages
queue-1-dlq: 2 messages
queue-2: 0 messages
queue-2-dlq: 0 messages
```

### Features

- **Automatic DLQ Discovery**: The script automatically finds and includes dead letter queue message counts
- **Error Handling**: Failed queue operations are logged to stderr and return `None`
- **Queue Name Input**: Accepts queue names (not full URLs) - AWS SDK handles URL resolution
- **Dual Interface**: Works both as a command-line tool and importable Python module

### Notes

- Dead letter queue names shouldn't be passed to the function - they're discovered automatically
- The script accepts queue names and uses AWS SDK to resolve full URLs automatically
- Any errors accessing queues are printed to stderr whilst continuing to process other queues
- Ensure your AWS credentials are configured with appropriate SQS permissions