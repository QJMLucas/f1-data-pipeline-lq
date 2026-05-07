import time
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def exponential_backoff_retry(
    func: Callable[..., T],
    max_retries: int = 2,
    base_delay: float = 20.0,
    max_delay: float = 60.0,
    backoff_factor: float = 2.0,
) -> T:
    """Execute function with exponential backoff retry logic.

    Args:
        func: Function to execute
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Multiplier for delay on each retry

    Returns:
        Result of function call

    Raises:
        Exception: If all retries are exhausted
    """
    for attempt in range(max_retries + 1):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries:
                logger.error(
                    f"All {max_retries + 1} attempts failed. Last error: {str(e)}"
                )
                raise

            delay = min(base_delay * (backoff_factor**attempt), max_delay)
            logger.warning(
                f"Attempt {attempt + 1} failed: {str(e)}. "
                f"Retrying in {delay:.1f}s..."
            )
            time.sleep(delay)
