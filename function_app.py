import azure.functions as func
import logging
import os
from common import get_secrets_from_vault, local_test
from mileage_calculation import main as calculate_mileage

app = func.FunctionApp()


@app.timer_trigger(
    schedule="0 12 */12 * * *",
    arg_name="myTimer",
    run_on_startup=False,
    use_monitor=True,
)
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Python timer trigger function executed.")

    if os.environ.get("AZURE_FUNCTIONS_ENVIRONMENT") == "Development":
        logging.info("Running in local development environment.")
        local_test()
    else:
        logging.info(
            "Running in production environment. Loading secrets from Azure Key Vault."
        )
        secret_names = [
            "AIRTABLE-API-KEY",
            "AIRTABLE-BASE-ID",
            "AIRTABLE-MILEAGE-TABLE-NAME",
            "GOOGLE-MAPS-API-KEY",
            "START-ADDRESS",
        ]
        get_secrets_from_vault(secret_names)

    calculate_mileage()
    logging.info("Mileage calculation completed successfully.")


@app.timer_trigger(
    schedule="0 12 */12 * * *",
    arg_name="secondtimer",
    run_on_startup=False,
    use_monitor=True,
)
def timer2(secondtimer: func.TimerRequest) -> None:
    logging.info("Second timer executed.")
