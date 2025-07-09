variable "queue_names" {
  description = "List of names as a list of strings."
  type        = list(string)
  default     = ["red-queue", "green-queue"]
}

variable "create_roles" {
  description = "boolean that conditionally creates an IAM role for each policy."
  type = boolean
}