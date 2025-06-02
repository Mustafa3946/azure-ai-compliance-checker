import json
import subprocess
import unittest

class TestTerraformOutputs(unittest.TestCase):
    def test_terraform_outputs(self):
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
