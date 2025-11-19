"""
JSON-based storage for watch items.
"""
import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from src.storage.models import WatchItem
from src.utils.logger import logger


class JSONStorage:
    """
    Manages persistent storage of watch items in JSON format.
    """
    
    def __init__(self, file_path: str = "items.json"):
        """
        Initialize JSON storage.
        
        Args:
            file_path: Path to JSON file
        """
        self.file_path = Path(file_path)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self) -> None:
        """Create empty JSON file if it doesn't exist."""
        if not self.file_path.exists():
            self.save([])
            logger.info(f"Created new storage file: {self.file_path}")
    
    def load(self) -> List[WatchItem]:
        """
        Load all items from storage.
        
        Returns:
            List of WatchItem objects
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                items = [WatchItem.from_dict(item_dict) for item_dict in data]
                logger.debug(f"Loaded {len(items)} items from {self.file_path}")
                return items
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from {self.file_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error loading items: {e}")
            return []
    
    def save(self, items: List[WatchItem]) -> bool:
        """
        Save items to storage.
        
        Args:
            items: List of WatchItem objects to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create backup before overwriting
            if self.file_path.exists() and self.file_path.stat().st_size > 0:
                backup_path = self.file_path.with_suffix('.json.bak')
                self.file_path.rename(backup_path)
                logger.debug(f"Created backup: {backup_path}")
            
            # Write new data
            data = [item.to_dict() for item in items]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved {len(items)} items to {self.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save items: {e}")
            return False
    
    def add(self, item: WatchItem) -> bool:
        """
        Add a single item to storage.
        
        Args:
            item: WatchItem to add
            
        Returns:
            True if successful
        """
        items = self.load()
        items.append(item)
        return self.save(items)
    
    def update_by_url(self, updated_item: WatchItem) -> bool:
        """
        Update an item identified by URL.
        
        Args:
            updated_item: Item with updated data
            
        Returns:
            True if item was found and updated
        """
        items = self.load()
        for i, item in enumerate(items):
            if item.url == updated_item.url:
                items[i] = updated_item
                self.save(items)
                logger.debug(f"Updated item: {updated_item.url}")
                return True
        
        logger.warning(f"Item not found for update: {updated_item.url}")
        return False
    
    def remove_by_url(self, url: str) -> bool:
        """
        Remove an item by URL.
        
        Args:
            url: URL of item to remove
            
        Returns:
            True if item was found and removed
        """
        items = self.load()
        original_count = len(items)
        items = [item for item in items if item.url != url]
        
        if len(items) < original_count:
            self.save(items)
            logger.info(f"Removed item: {url}")
            return True
        
        return False
    
    def find_by_url(self, url: str) -> Optional[WatchItem]:
        """
        Find an item by URL.
        
        Args:
            url: URL to search for
            
        Returns:
            WatchItem if found, None otherwise
        """
        items = self.load()
        for item in items:
            if item.url == url:
                return item
        return None
    
    def clear(self) -> bool:
        """
        Clear all items from storage.
        
        Returns:
            True if successful
        """
        return self.save([])
