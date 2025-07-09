terraform {
    required_version = ">= 1.0.0"

    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 3.48.0"
        }
    }
}

# this module is the dead letter queue
resource "aws_sqs_queue" "dlq" {
    for_each = toset(var.queue_names)
    name    = "${each.key}-dlq"
}

# this module creates the main queue with dql attached
resource "aws_sqs_queue" "main_queue" {
    for_each = toset(var.queue_names)

    name     = each.key
    
    redrive_policy = jsonencode({
        deadLetterTargetArn = aws_sqs_queue.dlq[each.key].arn
        maxReceiveCount     = 5
    })

    tags = {
        Name = each.key
    }
}

# creating IAM policies to consume and write to the sqs queues
resource "aws_iam_policy" "sqs_consumer_policy" {
    for_each = toset(var.queue_names)

    name        = "${each.key}-consumer-policy"
    description = "Policy to allow consuming messages from ${each.key} SQS queue"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect   = "Allow"
                Action   = ["sqs:ReceiveMessage", "sqs:DeleteMessage"]
                Resource = aws_sqs_queue.main_queue[each.key].arn
            }
        ]
    })
}

resource "aws_iam_policy" "sqs_producer_policy" {
    for_each = toset(var.queue_names)

    name        = "${each.key}-producer-policy"
    description = "Policy to allow sending messages to ${each.key} SQS queue"

    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Effect   = "Allow"
                Action   = ["sqs:SendMessage"]
                Resource = aws_sqs_queue.main_queue[each.key].arn
            }
        ]
    })
}