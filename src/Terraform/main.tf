# Build infrastructure
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)

  project = var.project
  region  = var.region
  zone    = var.zone
}

# VPC-networkin rakennus
resource "google_compute_network" "vpc_network" {
  name                    = "tuntikirjaus-vpc"
  auto_create_subnetworks = true
}

# Subnetworkin lisääminen
resource "google_compute_subnetwork" "network-with-private-secondary-ip-ranges" {
  name          = "tuntikirjaus-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  network       = google_compute_network.vpc_network.id

  secondary_ip_range {
    range_name    = "tf-test-secondary-range-update1"
    ip_cidr_range = "192.168.10.0/24"
  }
}

# Firewall-säännöt 
resource "google_compute_firewall" "default" {
  name    = "tuntikirjaus-firewall"
  network = google_compute_network.vpc_network.id

  allow {
    protocol = "icmp"
  }

  allow {
    protocol = "tcp"
    ports    = ["22", "80", "443", "8080", "1000-2000", "5432"]
  }
  target_tags = ["tuntikirjaus-firewall-tag"]
}