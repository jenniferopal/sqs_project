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

    name = each.key
    delay_seconds = 90
    max_message_size = 2048
    message_retention_seconds = 86400 # 1 day
    receive_wait_time_seconds = 10
        
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

# creating IAM roles to consume and write to the sqs queues
resource "aws_iam_role" "sqs_consumer_role" {
    count = var.create_roles ? length(var.queue_names) : 0 # using count to create the condition)

    name = "${var.queue_names[count.index]}-consumer-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "sqs.amazonaws.com"
                }
            }
        ]
    })

}

resource "aws_iam_role" "sqs_producer_role" {
    count = var.create_roles ? length(var.queue_names) : 0 # using count to create the condition)

    name = "${var.queue_names[count.index]}-producer-role"
    assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
            {   
                Action = "sts:AssumeRole"
                Effect = "Allow"
                Principal = {
                    Service = "sqs.amazonaws.com"
                }
            }
        ]
    })
}

# this attaches the policies to the roles with conditions 
resource "aws_iam_role_policy_attachment" "consumer_policy_attachment" {
    count = var.create_roles ? length(var.queue_names) : 0 # using count to create the condition)
    role = aws_iam_role.sqs_consumer_role[count.index].name
    policy_arn = aws_iam_policy.sqs_consumer_policy[var.queue_names[count.index]].arn 
}

resource "aws_iam_role_policy_attachment" "producer_policy_attachment" {
    count = var.create_roles ? length(var.queue_names) : 0 # using count to create the condition)
    role = aws_iam_role.sqs_producer_role[count.index].name
    policy_arn = aws_iam_policy.sqs_producer_policy[var.queue_names[count.index]].arn 
}