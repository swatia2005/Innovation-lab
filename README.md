# Innovation Lab – One-Click Azure Environment Builder

## Overview

Innovation Lab is a simple web application that allows users to create and manage Azure environments with a few clicks.

The application uses:

* Python Flask for the web interface
* Terraform for Infrastructure as Code (IaC)
* Microsoft Azure for cloud resources

The goal is to provide a quick and easy way to deploy development, testing, or hackathon environments without manually creating resources in Azure.

---

## Features

### Create Environment

Using the web interface, users can:

* Create a new Azure Resource Group
* Deploy a Virtual Machine
* Create a Storage Account
* Create an Azure Key Vault
* Reuse existing Virtual Networks and Subnets
* Optionally enable Disaster Recovery (DR) deployment

### Cleanup Environment

Users can remove resources created by Terraform through the Cleanup option without affecting shared infrastructure.

### Terraform Automation

The application automatically:

* Runs Terraform commands
* Maintains separate state files for each environment
* Displays deployment logs in the UI
* Supports repeatable and consistent deployments

---

## Architecture

User → Flask Web UI → Terraform → Azure Resources

Resources that can be deployed:

* Azure Resource Group
* Azure Virtual Machine
* Azure Storage Account
* Azure Key Vault

Existing shared infrastructure such as Virtual Networks and Subnets can be reused instead of recreated.

---

## Project Structure

```text
.
├── app.py
├── main.tf
├── variables.tf
├── outputs.tf
├── requirements.txt
├── static/
├── .terraform.lock.hcl
└── README.md
```

### Files

| File             | Description                    |
| ---------------- | ------------------------------ |
| app.py           | Flask application and UI logic |
| main.tf          | Azure resource definitions     |
| variables.tf     | Terraform input variables      |
| outputs.tf       | Terraform outputs              |
| requirements.txt | Python dependencies            |
| static/          | Images and static content      |

---

## Prerequisites

Before running the application, install:

* Python 3.10+
* Terraform
* Azure CLI

Login to Azure:

```bash
az login
```

Verify Terraform:

```bash
terraform --version
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/swatia2005/Innovation-lab.git
cd Innovation-lab
```

Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open a browser:

```text
http://<server-ip>:5000
```

---

## Example Workflow

1. Open the web application.
2. Enter Azure resource information.
3. Click Create Environment.
4. Monitor deployment progress.
5. Access created Azure resources.
6. Use Cleanup when resources are no longer needed.

---

## Use Cases

* Hackathons
* Development environments
* Proof of Concepts (POCs)
* Training and learning labs
* Temporary cloud environments

---

## Future Enhancements

* Email notifications
* HTTPS support
* Azure App Service deployment
* Ansible integration
* User authentication
* Multi-region deployments

---

## Author

Created as part of the Innovation Lab initiative to simplify Azure environment provisioning using Terraform and Flask.

