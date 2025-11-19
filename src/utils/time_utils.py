"""
Utility functions for time parsing and formatting.
"""
import time
import re
from typing import Dict

def get_total_seconds(time_var: str) -> int:
    """
    Convert time string (e.g., '1j 5h 30m 15s') to total seconds.
    
    Args:
        time_var: Time string with units (j=days, h=hours, m=minutes, s=seconds)
        
    Returns:
        Total time in seconds
    """
    time_units: Dict[str, int] = {'j': 86400, 'h': 3600, 'm': 60, 's': 1}
    matches = re.findall(r'(\d+)([jhms])', time_var)
    
    time_in_seconds = sum(int(value) * time_units[unit] for value, unit in matches)
    
    return time_in_seconds

def get_difference_with_pull_time(pull_time: float, time_var: str) -> float:
    """
    Calculate remaining time by comparing current time with pull time.
    
    Args:
        pull_time: Unix timestamp when data was pulled
        time_var: Original time string
        
    Returns:
        Remaining time in seconds (can be negative if expired)
    """
    time_diff = time.time() - pull_time
    time_in_seconds = get_total_seconds(time_var)
    remaining_time = time_in_seconds - time_diff
    return remaining_time

def get_time_var_from_seconds(seconds: float) -> str:
    """
    Convert seconds to human-readable time string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string (e.g., '1j 5h 30m 15s')
    """
    time_units: Dict[str, int] = {'j': 86400, 'h': 3600, 'm': 60, 's': 1}
    time_var = ''
    for unit in time_units:
        if seconds >= time_units[unit]:
            time_var += str(round(seconds // time_units[unit])) + unit + ' '
            seconds = seconds % time_units[unit]
    return time_var.strip()