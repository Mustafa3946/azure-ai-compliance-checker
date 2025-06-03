from azure.storage.blob import BlobServiceClient, ContentSettings
import os

# Azure Storage account details
account_name = "aicompliancedemost"
container_name = "reports"
report_path = "./output/report.html"

# Ensure output directory exists
os.makedirs(os.path.dirname(report_path), exist_ok=True)

# If report.html doesn't exist, create a simple HTML report
if not os.path.isfile(report_path):
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("""<!DOCTYPE html>
<html>
<head><title>Compliance Report</title></head>
<body>
<h1>AI Compliance Report</h1>
<p>This is a generated compliance report.</p>
</body>
</html>""")
    print(f"Created missing report file at {report_path}")

# Get connection string from environment
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

if not connection_string:
    raise Exception("Set the AZURE_STORAGE_CONNECTION_STRING environment variable")

# Connect to the blob service
blob_service = BlobServiceClient.from_connection_string(connection_string)

# Upload to 'reports' container
reports_container = blob_service.get_container_client(container_name)
with open(report_path, "rb") as report_file:
    reports_container.upload_blob(
        name="report.html",
        data=report_file,
        overwrite=True,
        content_settings=ContentSettings(content_type="text/html")
    )

# Upload to $web for static site
web_container = blob_service.get_container_client("$web")
with open(report_path, "rb") as report_file:
    web_container.upload_blob(
        name="index.html",
        data=report_file,
        overwrite=True,
        content_settings=ContentSettings(content_type="text/html")
    )

print("Report uploaded to both 'reports/report.html' and static website as 'index.html'")
