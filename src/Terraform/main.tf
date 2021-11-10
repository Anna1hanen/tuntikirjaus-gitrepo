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
  auto_create_subnetworks = false
}

# Subnetworkin lisääminen
resource "google_compute_subnetwork" "vpc_subnetwork" {
  name          = "tuntikirjaus-subnetwork"
  ip_cidr_range = "10.2.0.0/16"
  region        = var.region
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
    ports    = ["22", "80", "8080", "1000-2000"]
  }
  target_tags = ["tuntikirjaus-firewall-tag"]
}


# VM-instanssin luonti
resource "google_compute_instance" "vm_instance" {
  name         = "tuntikirjaus-instance"
  machine_type = "f1-micro"
  tags         = ["tuntikirjaus-firewall-tag"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-9"
    }
  }
  network_interface {
    network    = google_compute_network.vpc_network.id
    subnetwork = google_compute_subnetwork.vpc_subnetwork.id
    access_config {
      // Ephemeral public IP
    }
  }
  metadata_startup_script = file("startup-script.sh")
}

# #SQL instanssin luonti

# resource "google_sql_database_instance" "master" {
#   name             = "tuntikirjaus-proj-sql"
#   database_version = "POSTGRES_13"

#   settings {
#     tier = var.tier
#   }
# }

# # Databasen luonti
# resource "google_sql_database" "database" {
#   name     = "tuntikirjaus-database"
#   instance = "tuntikirjaus-proj-sql"
# }
