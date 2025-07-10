variable "queue_names" {
  description = "List of names as a list of strings."
  type        = list(string)
  default     = ["queue-1", "queue-2", "queue-3"]
}

variable "create_roles" {
  description = "boolean that conditionally creates an IAM role for each policy."
  type = bool
  default = true # setting to true to create iam roles for the queues  
}