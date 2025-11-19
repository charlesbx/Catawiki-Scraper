"""
Data models for auction items and related entities.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class WatchItem:
    """
    Represents a watch listing from Catawiki.

    Attributes:
        title: Watch title/description
        price: Current bid price (with currency symbol)
        time: Remaining auction time string (e.g., "1j 5h 30m")
        url: Direct link to the auction
        estimated_price: Price range estimate (e.g., "5000 € - 7000 €")
        pull_time: Unix timestamp when data was scraped
        reserve_price: Reserve price status
        item_id: Optional unique identifier
    """

    title: str
    price: str
    time: str
    url: str
    estimated_price: str
    pull_time: float
    reserve_price: str
    item_id: Optional[str] = None

    def __post_init__(self):
        """Generate item_id from URL if not provided."""
        if not self.item_id and self.url:
            # Extract ID from URL (e.g., /l/98500195-... -> 98500195)
            parts = self.url.split("/")
            for part in parts:
                if part.startswith("l-") or "-" in part:
                    self.item_id = part.split("-")[0].replace("l", "")
                    break

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WatchItem":
        """Create WatchItem from dictionary."""
        return cls(**data)

    @property
    def is_valid_price(self) -> bool:
        """Check if item has a valid price."""
        return self.price != "No price"

    @property
    def is_valid_time(self) -> bool:
        """Check if item has valid time remaining."""
        return self.time != "No time"

    @property
    def has_estimated_price(self) -> bool:
        """Check if item has estimated price range."""
        return self.estimated_price != "No estimated price"

    @property
    def reserve_met(self) -> bool:
        """Check if reserve price is met or doesn't exist."""
        return self.reserve_price in ["Reserve price reached", "No reserve price"]

    def get_price_numeric(self) -> Optional[float]:
        """
        Extract numeric price value.

        Returns:
            Price as float, or None if invalid
        """
        if not self.is_valid_price:
            return None
        try:
            # Remove currency symbols and spaces, handle special chars
            clean_price = self.price.replace(" €", "").replace("€", "")
            clean_price = clean_price.replace("\xa0", "").replace(" ", "")
            return float(clean_price)
        except (ValueError, AttributeError):
            return None

    def get_estimated_range(self) -> Optional[tuple[float, float]]:
        """
        Extract estimated price range.

        Returns:
            Tuple of (low, high) prices, or None if invalid
        """
        if not self.has_estimated_price:
            return None
        try:
            # Split range: "5000 € - 7000 €"
            low_str, high_str = self.estimated_price.split(" - ")
            low = float(
                low_str.replace(" €", "").replace("€", "").replace("\xa0", "").replace(" ", "")
            )
            high = float(
                high_str.replace(" €", "").replace("€", "").replace("\xa0", "").replace(" ", "")
            )
            return (low, high)
        except (ValueError, AttributeError):
            return None

    def get_median_estimate(self) -> Optional[float]:
        """Get median of estimated price range."""
        price_range = self.get_estimated_range()
        if price_range:
            return (price_range[0] + price_range[1]) / 2
        return None


@dataclass
class DealAlert:
    """
    Represents a deal notification to be sent.

    Attributes:
        item: The watch item
        alert_type: Type of alert (new, updated, closing)
        message: Formatted message text
        created_at: When the alert was created
    """

    item: WatchItem
    alert_type: str  # 'new', 'updated', 'closing'
    message: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "item": self.item.to_dict(),
            "alert_type": self.alert_type,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }
