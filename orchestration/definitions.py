import logging
from datetime import datetime, timezone
from dagster import asset, ScheduleDefinition, Definitions, MaterializeResult, MetadataValue, define_asset_job

from src.ingestion.drivers import get_drivers
from src.ingestion.laps import get_laps

logger = logging.getLogger(__name__)


@asset
def drivers_asset():
    """Fetch and store drivers data from OpenF1 API."""
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Starting drivers data ingestion at {timestamp}")
    result = get_drivers()
    print(f"Completed drivers data ingestion at {timestamp}. Records: {len(result)}")

    return MaterializeResult(
        value=result,
        metadata={
            "timestamp": MetadataValue.text(timestamp),
            "record_count": MetadataValue.int(len(result)),
        }
    )


@asset
def laps_asset(drivers_asset):
    """Fetch and store laps data from OpenF1 API.

    Depends on drivers_asset to ensure sequential execution.
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"Starting laps data ingestion at {timestamp}")
    result = get_laps(lap_number=8)
    print(f"Completed laps data ingestion at {timestamp}. Records: {len(result)}")

    return MaterializeResult(
        value=result,
        metadata={
            "timestamp": MetadataValue.text(timestamp),
            "record_count": MetadataValue.int(len(result)),
        }
    )


f1_data_pipeline = define_asset_job(
    "f1_data_pipeline",
    selection=[drivers_asset, laps_asset],
)

daily_schedule = ScheduleDefinition(
    job=f1_data_pipeline,
    cron_schedule="0 0 * * *",
    execution_timezone="UTC",
)

defs = Definitions(
    assets=[drivers_asset, laps_asset],
    jobs=[f1_data_pipeline],
    schedules=[daily_schedule],
)
