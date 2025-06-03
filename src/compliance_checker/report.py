import os
from datetime import datetime, timezone
from typing import Dict, Any
from html import escape
from azure.storage.blob import BlobServiceClient, ContentSettings

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_STORAGE_CONTAINER = "$web"
AZURE_STORAGE_ACCOUNT_NAME = "aicompliancedemost"
AZURE_BLOB_NAME = "index.html"


def generate_markdown_report(results: Dict[str, Any], output_path: str = "data/results/compliance_report.md") -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat() + "Z"
    lines = [
        "# Compliance Report",
        f"Generated: {timestamp}",
        "---",
    ]

    for module_name, findings in results.items():
        lines.append(f"## {module_name.capitalize()} Scan Results")

        if not findings:
            lines.append("No issues detected.\n")
            continue

        if isinstance(findings, dict):
            for key, value in findings.items():
                lines.append(f"### {key}")
                if isinstance(value, list) and value:
                    for item in value:
                        lines.append(f"- {item}")
                else:
                    lines.append(f"- {value}")
                lines.append("")
        elif isinstance(findings, list):
            for item in findings:
                if isinstance(item, dict):
                    item_str = ", ".join(f"{k}: {v}" for k, v in item.items())
                    lines.append(f"- {item_str}")
                else:
                    lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append(f"- {findings}\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"Report saved to {output_path}")


def generate_html_report(results: Dict[str, Any], output_path: str = "data/results/index.html") -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat() + "Z"

    html_parts = [
        "<!DOCTYPE html>",
        "<html lang='en'>",
        "<head>",
        "  <meta charset='UTF-8'>",
        "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
        "  <title>Compliance Report</title>",
        "  <style>",
        "    body { font-family: Arial, sans-serif; margin: 20px; padding: 0; background: #f9f9f9; }",
        "    h1, h2, h3 { color: #2c3e50; }",
        "    pre { background: #ecf0f1; padding: 10px; border-radius: 5px; }",
        "    ul { list-style-type: disc; margin-left: 20px; }",
        "    hr { border: none; border-top: 1px solid #bdc3c7; margin: 20px 0; }",
        "  </style>",
        "</head>",
        "<body>",
        f"<h1>Compliance Report</h1>",
        f"<p><em>Generated: {timestamp}</em></p>",
        "<hr>"
    ]

    for module_name, findings in results.items():
        html_parts.append(f"<h2>{escape(module_name.capitalize())} Scan Results</h2>")

        if not findings:
            html_parts.append("<p>No issues detected.</p>")
            continue

        if isinstance(findings, dict):
            for key, value in findings.items():
                html_parts.append(f"<h3>{escape(key)}</h3>")
                if isinstance(value, list) and value:
                    html_parts.append("<ul>")
                    for item in value:
                        html_parts.append(f"<li>{escape(str(item))}</li>")
                    html_parts.append("</ul>")
                else:
                    html_parts.append(f"<p>{escape(str(value))}</p>")
        elif isinstance(findings, list):
            html_parts.append("<ul>")
            for item in findings:
                if isinstance(item, dict):
                    item_str = ", ".join(f"{escape(str(k))}: {escape(str(v))}" for k, v in item.items())
                    html_parts.append(f"<li>{item_str}</li>")
                else:
                    html_parts.append(f"<li>{escape(str(item))}</li>")
            html_parts.append("</ul>")
        else:
            html_parts.append(f"<p>{escape(str(findings))}</p>")

    html_parts.append("</body></html>")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_parts))

    print(f"HTML report saved to {output_path}")

    if AZURE_STORAGE_CONNECTION_STRING:
        try:
            print("Uploading index.html to Azure Blob Storage using SDK...")
            blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=AZURE_STORAGE_CONTAINER, blob=AZURE_BLOB_NAME)

            with open(output_path, "rb") as data:
                blob_client.upload_blob(
                    data,
                    overwrite=True,
                    content_settings=ContentSettings(content_type='text/html')
                )

            print("Upload successful. You can view the report at:")
            print(f"https://{AZURE_STORAGE_ACCOUNT_NAME}.z8.web.core.windows.net/{AZURE_BLOB_NAME}")
        except Exception as e:
            print(f"Failed to upload to Azure Blob Storage: {e}")
    else:
        print("Azure Storage connection string not found in environment variable 'AZURE_STORAGE_CONNECTION_STRING'.")
