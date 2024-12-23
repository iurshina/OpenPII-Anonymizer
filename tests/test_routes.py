import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from anonymizer.main import app

client = TestClient(app)

class TestAnonymizeRoute(unittest.TestCase):

    @patch("anonymizer.llm.azure_llm.anonymize_text")
    def test_anonymize_route_success(self, mock_anonymize_text):
        """
        Test the /anonymize route for successful anonymization.
        """
        # Mock the response from the anonymize_text function
        mock_response = {
            "anonymized_text": "<Person 1> lives in <Location 1>. <PUBLIC>The library on Main Street is open to the public.</PUBLIC>",
            "resolved_entities": [
                {"placeholder": "<Person 1>", "original": "John", "type": "PERSON"},
                {"placeholder": "<Location 1>", "original": "New York", "type": "LOCATION"}
            ],
            "public_info": [
                {"text": "The library on Main Street", "start": 33, "end": 61}
            ]
        }
        mock_anonymize_text.return_value = mock_response

        # Input payload
        payload = {
            "input_text": "John lives in New York. The library on Main Street is open to the public.",
            "pii_types": ["person", "location"]
        }

        # Send POST request to /anonymize
        response = client.post("/anonymize", json=payload)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "anonymized_text": "<Person 1> lives in <Location 1>. <PUBLIC>The library on Main Street is open to the public.</PUBLIC>",
            "redacted_pii": ["John", "New York"]
        })
        mock_anonymize_text.assert_called_once_with(payload["input_text"])

    @patch("anonymizer.llm.azure_llm.anonymize_text")
    def test_anonymize_route_error(self, mock_anonymize_text):
        """
        Test the /anonymize route for error handling when anonymize_text fails.
        """
        # Mock an exception in the anonymize_text function
        mock_anonymize_text.side_effect = Exception("Error in anonymization pipeline")

        # Input payload
        payload = {
            "input_text": "John lives in New York. The library on Main Street is open to the public.",
            "pii_types": ["person", "location"]
        }

        # Send POST request to /anonymize
        response = client.post("/anonymize", json=payload)

        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertIn("detail", response.json())  # Check for error detail in the response
        self.assertEqual(response.json()["detail"], "Internal Server Error")
        mock_anonymize_text.assert_called_once_with(payload["input_text"])

if __name__ == "__main__":
    unittest.main()
