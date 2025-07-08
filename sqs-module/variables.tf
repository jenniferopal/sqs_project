variable "aws_region" {
  description = "The AWS region in which to create the SQS queue."
  type        = string
  default     = "us-east-1"
}

variable "queue_names" {
  description = "List of names as a list of strings."
  type        = list(string)
  default     = ["red-queue", "green-queue"]
}

