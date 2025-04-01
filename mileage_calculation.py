import os
from pyairtable import Api
from common import GoogleMapsDistanceCalculator


# Load environment variables
# load_dotenv()

# airtable = Table(AIRTABLE_API_KEY, AIRTABLE_BASE_ID, AIRTABLE_TABLE_NAME)
# lob_client = lob.Client(api_key=LOB_API_KEY)


def main():
    """
    Main function to calculate and update mileage for records in Airtable.
    This function performs the following steps:
    1. Retrieves all records from Airtable.
    2. Filters records where the 'Mileage' field is empty and 'Office Address' is not None.
    3. For each filtered record:
        a. Extracts the 'Mileage' and 'Office Address' fields.
        b. Calculates the round-trip mileage from a fixed start address to the office address.
        c. Updates the 'Mileage' field in Airtable with the calculated round-trip mileage.
    Note:
    - The start address is hardcoded as "210 Bartholomew St, Peabody, MA".
    - The Google Maps API key must be provided in the variable `GOOGLE_MAPS_API_KEY`.
    - The `GoogleMapsDistanceCalculator` class is used to calculate distances using the Google Maps API.
    """

    # Initialize clients
    AIRTABLE_API_KEY = os.getenv("AIRTABLE-API-KEY")
    AIRTABLE_BASE_ID = os.getenv("AIRTABLE-BASE-ID")
    AIRTABLE_TABLE_NAME = os.getenv("AIRTABLE-MILEAGE-TABLE-NAME")
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE-MAPS-API-KEY")

    airtable_api = Api(AIRTABLE_API_KEY)
    airtable_base = airtable_api.base(AIRTABLE_BASE_ID)
    airtable = airtable_base.table(AIRTABLE_TABLE_NAME)

    # Get all records from Airtable
    records = airtable.all()

    # Filter records where mileage field is empty
    records = [
        record
        for record in records
        if record["fields"].get("Mileage") is None
        and record["fields"].get("Office Address") is not None
    ]

    for record in records:
        fields = record["fields"]
        record_id = record["id"]

        # Extract mileage
        # mileage = fields.get("Mileage")
        address = fields.get("Office Address")

        # Calculate Mileage
        start_address = "210 Bartholomew St, Peabody, MA"
        end_address = address[0]
        client = GoogleMapsDistanceCalculator(GOOGLE_MAPS_API_KEY)
        to_mileage_value = client.calculate_distance(
            start_address=start_address, end_address=end_address
        )
        from_mileage_value = client.calculate_distance(
            start_address=end_address, end_address=start_address
        )
        round_trip_mileage = to_mileage_value + from_mileage_value

        # if verified['is_valid']:
        if round_trip_mileage:
            changes = {}
            changes["Mileage"] = round_trip_mileage

            # Update Airtable if changes exist
            if changes:
                # changes['Deliverability'] = verified['deliverability']
                print(f"Updating record {record_id} with changes: {changes}")
                airtable.update(record_id, changes)


if __name__ == "__main__":
    main()
