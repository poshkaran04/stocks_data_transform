locals {
  data_lake_bucket = "bootcamp_data_lake"
}

variable "project" {
  description = "data-bootcamp-380922"
}

variable "region" {
  description = "Region for GCP resources. I have taken Frankfurt given the GDPR regulations."
  default = "europe-west3"
  type = string
}

variable "storage_class" {
  description = "Storage class type for my bucket."
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset where my raw data (from GCS) will be written to"
  type = string
  default = "us_stocks"
}
