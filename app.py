from flask import Flask, request
import subprocess
import re
import os
import html

app = Flask(__name__)

TERRAFORM_DIR = "."
APP_LOCK_FILE = "/tmp/hackathon_terraform.lock"


def safe_state_name(resource_group_name):
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "-", resource_group_name)
    return f"terraform-{safe_name}.tfstate"


def is_terraform_running():
    result = subprocess.run(
        ["pgrep", "-f", "terraform"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def lock_exists():
    return os.path.exists(APP_LOCK_FILE)


def create_lock():
    with open(APP_LOCK_FILE, "w") as f:
        f.write("Terraform deployment in progress")


def remove_lock():
    if os.path.exists(APP_LOCK_FILE):
        os.remove(APP_LOCK_FILE)


def run_terraform(command):
    create_lock()
    try:
        result = subprocess.run(
            command,
            cwd=TERRAFORM_DIR,
            capture_output=True,
            text=True,
            timeout=900
        )
        return result
    except subprocess.TimeoutExpired as e:
        return subprocess.CompletedProcess(
            command,
            returncode=124,
            stdout=e.stdout or "",
            stderr="Terraform command timed out after 15 minutes."
        )
    finally:
        remove_lock()


def terraform_busy_message():
    return """
    <h3>Terraform is already running</h3>
    <p>Please do not click Create Environment or Cleanup again until the current operation finishes.</p>
    <br><a href="/">Go Back</a>
    """

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>CIBC Hackathon 2026 - One Click Environment</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 30px;
                background-color: #f8f9fa;
            }

            .header {
                text-align: center;
                margin-bottom: 30px;
            }

            .header img {
                width: 250px;
                margin-bottom: 10px;
            }

            .header h1 {
                color: #b61f29;
                margin-bottom: 5px;
            }

            .header h3 {
                color: #555;
                margin-top: 0;
            }

            .section {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }

            label {
                font-weight: bold;
            }

            input, select {
                padding: 8px;
                margin-top: 5px;
                margin-bottom: 10px;
                width: 300px;
            }

            input[type=submit] {
                background-color: #b61f29;
                color: white;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                border-radius: 5px;
                width: auto;
            }

            input[type=submit]:hover {
                background-color: #941821;
            }

            small {
                color: #666;
            }
        </style>
    </head>

    <body>

        <div class="header">
            <img src="/static/logo.png" alt="CIBC Logo">
            <h1>CIBC Hackathon 2026</h1>
            <h3>One Click Cloud Environment Provisioning Portal</h3>
        </div>

        <div class="section">

            <h2>Create Environment</h2>

            <form action="/deploy" method="post">

                <label>Resource Group Name:</label><br>
                <input name="resource_group_name" required><br><br>

                <label>Name Prefix:</label><br>
                <input name="name_prefix" value="hackathon" required>
                <small>Example: hackathon, demo, test</small><br><br>

                <label>Number of VMs:</label><br>
                <input type="number"
                       name="vm_count"
                       min="0"
                       max="20"
                       value="1"
                       required><br><br>

                <label>Number of Storage Accounts:</label><br>
                <input type="number"
                       name="storage_account_count"
                       min="0"
                       max="20"
                       value="1"
                       required><br><br>

                <label>Number of Key Vaults:</label><br>
                <input type="number"
                       name="key_vault_count"
                       min="0"
                       max="20"
                       value="1"
                       required><br><br>

                <label>Primary Region:</label><br>
                <select name="primary_location">
                    <option value="North Central US">North Central US</option>
                    <option value="Central US">Central US</option>
                    <option value="East US">East US</option>
                    <option value="East US 2">East US 2</option>
                    <option value="West US">West US</option>
                    <option value="South Central US">South Central US</option>
                </select>

                <br><br>

                <input type="submit" value="Create Environment">

            </form>

        </div>

        <div class="section">

            <h2>Cleanup Environment</h2>

            <form action="/cleanup" method="post">

                <label>Resource Group Name to Cleanup:</label><br>
                <input name="resource_group_name" required><br><br>

                <input type="submit" value="Cleanup">

            </form>

        </div>

    </body>
    </html>
    """


@app.route("/deploy", methods=["POST"])
def deploy():
    if lock_exists() or is_terraform_running():
        return terraform_busy_message()

    resource_group_name = request.form["resource_group_name"]
    name_prefix = request.form["name_prefix"]
    vm_count = request.form["vm_count"]
    storage_account_count = request.form["storage_account_count"]
    key_vault_count = request.form["key_vault_count"]
    primary_location = request.form["primary_location"]

    state_file = safe_state_name(resource_group_name)

    command = [
        "terraform", "apply", "-auto-approve",
        f"-state={state_file}",
        f"-var=resource_group_name={resource_group_name}",
        f"-var=name_prefix={name_prefix}",
        f"-var=vm_count={vm_count}",
        f"-var=storage_account_count={storage_account_count}",
        f"-var=key_vault_count={key_vault_count}",
        f"-var=primary_location={primary_location}"
    ]

    result = run_terraform(command)

    stdout = html.escape(result.stdout)
    stderr = html.escape(result.stderr)

    if result.returncode == 0:
        return f"""
        <h3>Environment Created Successfully</h3>
        <p>Resource Group: {html.escape(resource_group_name)}</p>
        <p>State File: {html.escape(state_file)}</p>
        <p>VM Count: {html.escape(vm_count)}</p>
        <p>Storage Account Count: {html.escape(storage_account_count)}</p>
        <p>Key Vault Count: {html.escape(key_vault_count)}</p>
        <pre>{stdout}</pre>
        <br><a href="/">Go Back</a>
        """
    else:
        return f"""
        <h3>Deployment Failed</h3>
        <p>State File: {html.escape(state_file)}</p>
        <pre>{stderr}</pre>
        <br><a href="/">Go Back</a>
        """


@app.route("/cleanup", methods=["POST"])
def cleanup():
    if lock_exists() or is_terraform_running():
        return terraform_busy_message()

    resource_group_name = request.form["resource_group_name"]
    state_file = safe_state_name(resource_group_name)

    command = [
        "az", "group", "delete",
        "--name", resource_group_name,
        "--yes",
        "--no-wait"
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    stdout = html.escape(result.stdout)
    stderr = html.escape(result.stderr)

    if result.returncode == 0:
        if os.path.exists(state_file):
            os.remove(state_file)

        backup_file = f"{state_file}.backup"
        if os.path.exists(backup_file):
            os.remove(backup_file)

        return f"""
        <h3>Cleanup Started Successfully</h3>
        <p>Resource Group deletion started: {html.escape(resource_group_name)}</p>
        <p>State File Removed: {html.escape(state_file)}</p>
        <p>Azure will delete the resources in the background.</p>
        <pre>{stdout}</pre>
        <br><a href="/">Go Back</a>
        """
    else:
        return f"""
        <h3>Cleanup Failed</h3>
        <p>Resource Group: {html.escape(resource_group_name)}</p>
        <pre>{stderr}</pre>
        <br><a href="/">Go Back</a>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
