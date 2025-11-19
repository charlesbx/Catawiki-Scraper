"""
Tests for the DealAnalyzer module.
"""
import pytest
import time
from src.storage.models import WatchItem
from src.analyzer.filters import DealAnalyzer, DealCriteria


class TestDealAnalyzer:
    """Test suite for DealAnalyzer."""
    
    def test_good_deal_detection(self):
        """Test that a good deal is correctly identified."""
        # Create a watch priced at 50% of estimate
        # Use current timestamp to simulate an active auction
        current_time = time.time()
        item = WatchItem(
            title="Rolex Submariner",
            price="5 000 €",
            time="20m",  # Less than 30min threshold
            url="https://example.com/item/123",
            estimated_price="9 000 € - 11 000 €",
            pull_time=current_time,
            reserve_price="No reserve price"
        )
        
        analyzer = DealAnalyzer()
        is_good, reason = analyzer.is_good_deal(item)
        
        # Should be a good deal (50% < 90% threshold)
        assert is_good, f"Expected good deal but got: {reason}"
    
    def test_expensive_item_rejected(self):
        """Test that expensive items are rejected."""
        # Create a watch priced at 95% of estimate
        current_time = time.time()
        item = WatchItem(
            title="Expensive Watch",
            price="9 500 €",
            time="30m",
            url="https://example.com/item/124",
            estimated_price="9 000 € - 11 000 €",
            pull_time=current_time,
            reserve_price="No reserve price"
        )
        
        analyzer = DealAnalyzer()
        is_good, reason = analyzer.is_good_deal(item)
        
        # Should NOT be a good deal (95% > 90% threshold)
        assert not is_good
        assert "too high" in reason.lower()
    
    def test_reserve_not_met_rejected(self):
        """Test that items with unmet reserve are rejected."""
        current_time = time.time()
        item = WatchItem(
            title="Rolex Submariner",
            price="5 000 €",
            time="30m",
            url="https://example.com/item/125",
            estimated_price="9 000 € - 11 000 €",
            pull_time=current_time,
            reserve_price="Reserve price not reached"
        )
        
        analyzer = DealAnalyzer()
        is_good, reason = analyzer.is_good_deal(item)
        
        assert not is_good
        assert "reserve" in reason.lower()
    
    def test_custom_criteria(self):
        """Test analyzer with custom criteria."""
        # Stricter criteria: 80% threshold instead of 90%
        criteria = DealCriteria(price_threshold=0.80)
        analyzer = DealAnalyzer(criteria)
        
        # Item at 85% of estimate
        current_time = time.time()
        item = WatchItem(
            title="Test Watch",
            price="8 500 €",
            time="30m",
            url="https://example.com/item/126",
            estimated_price="9 000 € - 11 000 €",
            pull_time=current_time,
            reserve_price="No reserve price"
        )
        
        is_good, reason = analyzer.is_good_deal(item)
        
        # Should be rejected with stricter criteria
        assert not is_good
    
    def test_deal_scoring(self):
        """Test deal quality scoring."""
        analyzer = DealAnalyzer()
        
        current_time = time.time()
        good_deal = WatchItem(
            title="Great Deal",
            price="5 000 €",
            time="30m",
            url="https://example.com/item/127",
            estimated_price="10 000 € - 12 000 €",
            pull_time=current_time,
            reserve_price="No reserve price"
        )
        
        okay_deal = WatchItem(
            title="Okay Deal",
            price="9 000 €",
            time="30m",
            url="https://example.com/item/128",
            estimated_price="10 000 € - 12 000 €",
            pull_time=current_time,
            reserve_price="No reserve price"
        )
        
        good_score = analyzer.get_deal_score(good_deal)
        okay_score = analyzer.get_deal_score(okay_deal)
        
        # Better deal should have lower score
        assert good_score < okay_score
        assert good_score < 0.5  # 5000/11000 ≈ 0.45


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
