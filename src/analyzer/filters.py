"""
Deal filtering and analysis logic.
"""

from typing import List, Optional
from dataclasses import dataclass

from src.storage.models import WatchItem
from src.utils.time_utils import get_difference_with_pull_time, get_total_seconds
from src.config.settings import PERCENTAGE_THRESHOLD, REMAINING_TIME_THRESHOLD
from src.utils.logger import logger


@dataclass
class DealCriteria:
    """
    Criteria for identifying good deals.

    Attributes:
        price_threshold: Maximum price as percentage of estimate (0.0-1.0)
        time_threshold: Maximum remaining time in seconds
        require_reserve_met: Only include items with met/no reserve
    """

    price_threshold: float = PERCENTAGE_THRESHOLD
    time_threshold: int = REMAINING_TIME_THRESHOLD
    require_reserve_met: bool = True


class DealAnalyzer:
    """
    Analyzes watch items to identify good deals.
    """

    def __init__(self, criteria: Optional[DealCriteria] = None):
        """
        Initialize analyzer with criteria.

        Args:
            criteria: Deal filtering criteria (uses defaults if None)
        """
        self.criteria = criteria or DealCriteria()
        logger.debug(
            f"DealAnalyzer initialized with threshold {self.criteria.price_threshold:.0%}, "
            f"time limit {self.criteria.time_threshold}s"
        )

    def is_good_deal(self, item: WatchItem) -> tuple[bool, Optional[str]]:
        """
        Determine if an item is a good deal.

        Args:
            item: WatchItem to analyze

        Returns:
            Tuple of (is_good_deal, reason_if_not)
        """
        # Check basic validity
        if not item.is_valid_price:
            return False, "No valid price"

        if not item.is_valid_time:
            return False, "No valid time"

        if not item.has_estimated_price:
            return False, "No estimated price"

        # Check reserve price if required
        if self.criteria.require_reserve_met and not item.reserve_met:
            return False, "Reserve price not met"

        # Get numeric values
        current_price = item.get_price_numeric()
        median_estimate = item.get_median_estimate()

        if current_price is None or median_estimate is None:
            return False, "Cannot parse price values"

        # Check price threshold
        price_ratio = current_price / median_estimate
        if price_ratio > self.criteria.price_threshold:
            return False, f"Price too high ({price_ratio:.1%} of estimate)"

        # Check time remaining
        remaining_time = get_difference_with_pull_time(item.pull_time, item.time)
        if remaining_time < 0:
            return False, "Auction ended"

        if remaining_time > self.criteria.time_threshold:
            return False, f"Too much time remaining ({remaining_time:.0f}s)"

        # It's a good deal!
        logger.debug(
            f"Good deal found: {item.title[:50]}... - "
            f"{price_ratio:.1%} of estimate, {remaining_time:.0f}s remaining"
        )
        return True, None

    def filter_good_deals(self, items: List[WatchItem]) -> List[WatchItem]:
        """
        Filter a list of items to only good deals.

        Args:
            items: List of WatchItem objects

        Returns:
            Filtered list of good deals
        """
        good_deals = []

        for item in items:
            is_good, reason = self.is_good_deal(item)
            if is_good:
                good_deals.append(item)

        logger.info(f"Found {len(good_deals)} good deals out of {len(items)} items")
        return good_deals

    def get_deal_score(self, item: WatchItem) -> float:
        """
        Calculate a deal score (lower price ratio = better deal).

        Args:
            item: WatchItem to score

        Returns:
            Score from 0.0 (best) to 1.0 (worst), or -1.0 if invalid
        """
        current_price = item.get_price_numeric()
        median_estimate = item.get_median_estimate()

        if current_price is None or median_estimate is None:
            return -1.0

        return current_price / median_estimate

    def sort_by_deal_quality(self, items: List[WatchItem]) -> List[WatchItem]:
        """
        Sort items by deal quality (best deals first).

        Args:
            items: List of WatchItem objects

        Returns:
            Sorted list (best deals first)
        """
        return sorted(
            items,
            key=lambda item: self.get_deal_score(item),
            reverse=False,  # Lower score = better deal
        )

    def get_urgent_items(
        self, items: List[WatchItem], urgency_threshold: int = 90
    ) -> List[WatchItem]:
        """
        Get items closing very soon.

        Args:
            items: List of WatchItem objects
            urgency_threshold: Seconds threshold for urgency

        Returns:
            Items closing within threshold
        """
        urgent = []

        for item in items:
            if not item.is_valid_time:
                continue

            remaining = get_difference_with_pull_time(item.pull_time, item.time)
            if 0 < remaining <= urgency_threshold:
                urgent.append(item)

        logger.info(f"Found {len(urgent)} urgent items (<{urgency_threshold}s)")
        return urgent
