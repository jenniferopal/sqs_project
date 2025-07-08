terraform {
    required_providers {
        aws = {
            source  = "hashicorp/aws"
            version = "~> 3.0"
        }
    }
    required_version = ">= 1.0.0"
}

provider "aws" {
  region = var.aws_region
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