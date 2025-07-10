# SQS Module

A Terraform module that creates SQS queues with dead letter queues and IAM policies.

## Usage

```hcl
module "sqs_queues" {
  source = "./sqs-module"
  
  queue_names  = ["processing-queue", "notification-queue"]
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

The `sqs_queues.py` script monitors message counts in your queues.

### Setup

1. Install boto3: `pip install boto3`
2. Configure AWS credentials
3. Update queue URLs in the script:
   ```python
   queues = [
       "https://sqs.us-east-1.amazonaws.com/YOUR-ACCOUNT-ID/your-queue-name"
   ]
   ```

### Run

```bash
python sqs_queues.py
```

### Output

```
Queue: processing-queue, Messages: 42
Queue: notification-queue, Messages: 0
```
