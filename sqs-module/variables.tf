variable "queue_names" {
  description = "List of names as a list of strings."
  type        = list(string)
  default     = ["red-queue", "green-queue"]
}