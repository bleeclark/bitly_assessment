#!/usr/bin/env python3
"""
Bitly Backend Engineer Coding Challenge Solution

This module implements a solution to calculate the number of clicks from 2021
for each record in the encodes.csv dataset using click event data from decodes.json.
"""

import csv
import json
import logging
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple, Any
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class ClickCounter:
    """
    A class to handle the processing of Bitly encode and decode data.
    
    This class provides methods to parse CSV and JSON data files,
    count clicks from 2021, and generate the required output format.
    """
    
    def __init__(self, encodes_file: str = "encodes.csv", decodes_file: str = "decodes.json"):
        """
        Initialize the ClickCounter with file paths.
        
        Args:
            encodes_file (str): Path to the encodes CSV file
            decodes_file (str): Path to the decodes JSON file
        """
        self.encodes_file = encodes_file
        self.decodes_file = decodes_file
        self.hash_to_url: Dict[str, str] = {}
        self.click_events: List[str] = []
        
    def parse_encodes(self) -> Dict[str, str]:
        """
        Parse encodes.csv to create a hash to long_url mapping.
        
        Returns:
            Dict[str, str]: Mapping of hash to long_url
            
        Raises:
            FileNotFoundError: If encodes file doesn't exist
            ValueError: If CSV format is invalid
        """
        logger.info(f"Parsing encodes file: {self.encodes_file}")
        
        if not os.path.exists(self.encodes_file):
            raise FileNotFoundError(f"Encodes file not found: {self.encodes_file}")
        
        hash_to_url = {}
        try:
            with open(self.encodes_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                # Validate required columns
                required_columns = {'long_url', 'hash'}
                if not required_columns.issubset(reader.fieldnames or set()):
                    raise ValueError(f"Missing required columns. Expected: {required_columns}, Found: {reader.fieldnames}")
                
                row_count = 0
                for row in reader:
                    row_count += 1
                    hash_value = row['hash'].strip()
                    long_url = row['long_url'].strip()
                    
                    if not hash_value or not long_url:
                        logger.warning(f"Skipping row {row_count}: empty hash or URL")
                        continue
                    
                    if hash_value in hash_to_url:
                        logger.warning(f"Duplicate hash found: {hash_value}")
                    
                    hash_to_url[hash_value] = long_url
                
                logger.info(f"Successfully parsed {row_count} rows from encodes file")
                logger.info(f"Found {len(hash_to_url)} unique hash-to-URL mappings")
                
        except Exception as e:
            logger.error(f"Error parsing encodes file: {e}")
            raise ValueError(f"Failed to parse encodes file: {e}")
        
        self.hash_to_url = hash_to_url
        return hash_to_url
    
    def parse_decodes(self) -> List[str]:
        """
        Parse decodes.json to extract click events from 2021.
        
        Returns:
            List[str]: List of bitlink hashes from 2021 click events
            
        Raises:
            FileNotFoundError: If decodes file doesn't exist
            ValueError: If JSON format is invalid
        """
        logger.info(f"Parsing decodes file: {self.decodes_file}")
        
        if not os.path.exists(self.decodes_file):
            raise FileNotFoundError(f"Decodes file not found: {self.decodes_file}")
        
        click_events = []
        try:
            with open(self.decodes_file, mode='r', encoding='utf-8') as file:
                data = json.load(file)
            
            if not isinstance(data, list):
                raise ValueError("Decodes file should contain a JSON array")
            
            total_events = 0
            events_2021 = 0
            
            for event in data:
                total_events += 1
                
                try:
                    # Extract bitlink hash from the bitlink URL
                    if 'bitlink' not in event:
                        logger.warning(f"Missing 'bitlink' in event {total_events}")
                        continue
                    
                    bitlink_url = event['bitlink'].strip()
                    if not bitlink_url:
                        logger.warning(f"Empty bitlink in event {total_events}")
                        continue
                    
                    # Extract hash from bitlink URL (e.g., "http://bit.ly/2kkAHNs" -> "2kkAHNs")
                    try:
                        # Parse the URL to extract the hash
                        import urllib.parse
                        parsed_url = urllib.parse.urlparse(bitlink_url)
                        if parsed_url.path:
                            # Remove leading slash and extract hash
                            bitlink_hash = parsed_url.path.lstrip('/')
                        else:
                            logger.warning(f"Could not extract hash from bitlink URL: {bitlink_url}")
                            continue
                    except Exception as e:
                        logger.warning(f"Error parsing bitlink URL {bitlink_url}: {e}")
                        continue
                    
                    # Parse timestamp and check if it's from 2021
                    if 'timestamp' not in event:
                        logger.warning(f"Missing 'timestamp' in event {total_events}")
                        continue
                    
                    timestamp_str = event['timestamp']
                    try:
                        # Parse ISO format timestamp with timezone
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                        if timestamp.year == 2021:
                            click_events.append(bitlink_hash)
                            events_2021 += 1
                    except ValueError as e:
                        logger.warning(f"Invalid timestamp format in event {total_events}: {timestamp_str} - {e}")
                        continue
                        
                except KeyError as e:
                    logger.warning(f"Missing key {e} in event {total_events}")
                    continue
            
            logger.info(f"Successfully parsed {total_events} total events")
            logger.info(f"Found {events_2021} click events from 2021")
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in decodes file: {e}")
            raise ValueError(f"Failed to parse JSON: {e}")
        except Exception as e:
            logger.error(f"Error parsing decodes file: {e}")
            raise ValueError(f"Failed to parse decodes file: {e}")
        
        self.click_events = click_events
        return click_events
    
    def count_clicks(self) -> Dict[str, int]:
        """
        Count clicks per hash for the year 2021.
        
        Returns:
            Dict[str, int]: Mapping of hash to click count
        """
        logger.info("Counting clicks per hash for 2021")
        
        click_counts = defaultdict(int)
        for hash_value in self.click_events:
            click_counts[hash_value] += 1
        
        logger.info(f"Found {len(click_counts)} unique hashes with clicks")
        return dict(click_counts)
    
    def map_clicks_to_urls(self, click_counts: Dict[str, int]) -> List[Dict[str, int]]:
        """
        Map click counts to their corresponding long URLs.
        
        Args:
            click_counts (Dict[str, int]): Mapping of hash to click count
            
        Returns:
            List[Dict[str, int]]: List of dictionaries with URL as key and count as value
        """
        logger.info("Mapping click counts to long URLs")
        
        url_clicks = []
        unmatched_hashes = 0
        
        for hash_value, count in click_counts.items():
            long_url = self.hash_to_url.get(hash_value)
            if long_url:
                url_clicks.append({long_url: count})
            else:
                logger.warning(f"No matching long URL found for hash: {hash_value}")
                unmatched_hashes += 1
        
        if unmatched_hashes > 0:
            logger.warning(f"Total unmatched hashes: {unmatched_hashes}")
        
        logger.info(f"Successfully mapped {len(url_clicks)} URLs with click counts")
        return url_clicks
    
    def sort_results(self, url_clicks: List[Dict[str, int]]) -> List[Dict[str, int]]:
        """
        Sort results by click count in descending order.
        
        Args:
            url_clicks (List[Dict[str, int]]): List of URL click count dictionaries
            
        Returns:
            List[Dict[str, int]]: Sorted list in descending order by click count
        """
        logger.info("Sorting results by click count (descending)")
        
        sorted_results = sorted(url_clicks, key=lambda x: list(x.values())[0], reverse=True)
        logger.info(f"Sorted {len(sorted_results)} results")
        return sorted_results
    
    def process(self) -> List[Dict[str, int]]:
        """
        Main processing method that orchestrates the entire workflow.
        
        Returns:
            List[Dict[str, int]]: Sorted array of JSON objects with URL and click count
        """
        logger.info("Starting click counting process")
        
        try:
            # Parse input files
            self.parse_encodes()
            self.parse_decodes()
            
            # Count clicks and map to URLs
            click_counts = self.count_clicks()
            url_clicks = self.map_clicks_to_urls(click_counts)
            
            # Sort results
            sorted_results = self.sort_results(url_clicks)
            
            logger.info("Click counting process completed successfully")
            return sorted_results
            
        except Exception as e:
            logger.error(f"Error in processing: {e}")
            raise


def main():
    """
    Main entry point for the script.
    
    Processes the encodes.csv and decodes.json files to calculate
    2021 click counts and outputs the results in the required format.
    """
    try:
        # Initialize the click counter
        counter = ClickCounter()
        
        # Process the data
        results = counter.process()
        
        # Output the results in the required JSON format
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
