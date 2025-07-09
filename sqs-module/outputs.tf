output "queue_arns" {
    description = "list of queue arns for the newly created queues"
    value       = { for k, v in aws_sqs_queue.main_queue : k => v.arn }
}

output "consume_policy_arn" {
    description = "the arn of a created IAM policy that allows sqs:receiveMessage and sqs:DeleteMessage on the created queues"
    value       = { for k, v in aws_iam_policy.sqs_consumer_policy : k => v.arn }
}

output "write_policy_arn" {
    description = "the arn of a created IAM policy that allows sqs:SendMessage to the created queues"
    value       = { for k, v in aws_iam_policy.sqs_producer_policy : k => v.arn }
}

