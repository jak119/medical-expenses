import googlemaps


class GoogleMapsDistanceCalculator:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def calculate_distance(self, start_address, end_address):
        try:
            directions_result = self.client.directions(
                start_address, end_address, units="imperial"
            )

            if directions_result and len(directions_result) > 0:
                distance_meters = directions_result[0]["legs"][0]["distance"]["value"]
                distance_miles = distance_meters / 1609.34  # Convert meters to miles
                return round(distance_miles, 2)

            return None
        except Exception as e:
            print(f"Error calculating distance: {e}")
            return None


class GoogleMapsTimeCalculator:
    def __init__(self, api_key):
        self.client = googlemaps.Client(key=api_key)

    def calculate_distance(self, start_address, end_address):
        try:
            directions_result = self.client.directions(
                start_address, end_address, units="imperial"
            )

            if directions_result and len(directions_result) > 0:
                distance_time = directions_result[0]["legs"][0]["duration"]["value"]
                return round(distance_time, 2) / 60

            return None
        except Exception as e:
            print(f"Error calculating time: {e}")
            return None


def get_secrets_from_vault(secret_names: list) -> None:
    from azure.identity import DefaultAzureCredential
    from azure.keyvault.secrets import SecretClient
    import os
    import logging

    """
    Retrieve secrets from Azure Key Vault and set them as environment variables
    Args:
        secret_names: List of secret names to retrieve
    """
    try:
        vault_name = os.environ.get("VAULT_NAME")
        if not vault_name:
            raise ValueError("VAULT_NAME environment variable is not set")

        vault_url = f"https://{vault_name}.vault.azure.net"
        credential = DefaultAzureCredential()
        secret_client = SecretClient(vault_url=vault_url, credential=credential)

        for secret_name in secret_names:
            try:
                secret = secret_client.get_secret(secret_name)
                os.environ[secret_name] = secret.value
                logging.info(f"Successfully loaded secret: {secret_name}")
            except Exception as e:
                logging.error(f"Failed to load secret {secret_name}: {str(e)}")

    except Exception as e:
        logging.error(f"Failed to initialize Key Vault client: {str(e)}")
        raise


def local_test():
    from dotenv import load_dotenv
    import logging
    import os

    # Load environment variables
    load_dotenv()
    logging.info(
        f"AIRTABLE-MILEAGE-TABLE-NAME: {os.getenv('AIRTABLE-MILEAGE-TABLE-NAME')}"
    )
