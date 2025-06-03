"""
test_terraform_outputs.py

Unit tests for verifying Terraform outputs after deployment.
Ensures that key Azure resource outputs are present and correctly formatted.

Functions:
    - test_terraform_outputs: Runs 'terraform output -json' and checks for required outputs.
"""

import json
import subprocess
import unittest

class TestTerraformOutputs(unittest.TestCase):
    """
    Test suite for validating Terraform output values.
    """

    def test_terraform_outputs(self):
        """
        Runs 'terraform output -json' in the infra/terraform directory and checks for expected outputs.
        """
        # Run 'terraform output -json'
        result = subprocess.run(
            ["terraform", "output", "-json"],
            cwd="infra/terraform",
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, "Terraform output command failed")
        
        outputs = json.loads(result.stdout)
        self.assertIn("resource_group_name", outputs)
        self.assertIn("storage_account_name", outputs)
        self.assertTrue(outputs["resource_group_name"]["value"].startswith("ai-compliance"))
        self.assertTrue("aicompliance" in outputs["storage_account_name"]["value"])

if __name__ == "__main__":
    unittest.main()
