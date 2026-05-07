from src.ingestion.api_client import F1APIClient


class TestF1APIClient:
    def test_api_client_can_fetch_drivers(self):
        """Test that client can fetch drivers from real API"""
        print("\n=== Starting test: test_api_client_can_fetch_drivers ===")

        client = F1APIClient()
        print(f"✓ Created client with base_url: {client.base_url}")

        print(
            "\n→ Calling client.get('drivers', params={'driver_number': 55, 'session_key': 9159})..."
        )
        data = client.get("drivers", params={"driver_number": 55, "session_key": 9159})
        print("✓ Got response from API")

        client.close()
        print("✓ Closed session")

        # Verify response is valid
        print("\n--- Verification ---")
        assert isinstance(data, list), "Response should be a list"
        print("✓ Response is a list")

        assert len(data) > 0, "Response should contain at least one driver"
        print(f"✓ Got {len(data)} drivers")

        assert "driver_number" in data[0], "Missing 'driver_number' field"
        print("✓ First driver has 'driver_number' field")

        print("\n✓ TEST PASSED!\n")
