import os
from datetime import datetime, timezone
from typing import Dict, Any

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
                # If list items are dicts, pretty print key-values:
                if isinstance(item, dict):
                    item_str = ", ".join(f"{k}: {v}" for k, v in item.items())
                    lines.append(f"- {item_str}")
                else:
                    lines.append(f"- {item}")
            lines.append("")
        else:
            # For any other data type, just print it
            lines.append(f"- {findings}\n")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

    print(f"Report saved to {output_path}")
