#!/usr/bin/env python3
"""
Unit tests for the ClickCounter class.

This module contains comprehensive unit tests for all functions
in the click_counter module.
"""

import unittest
import json
import tempfile
import os
import csv
from unittest.mock import patch, mock_open
from click_counter import ClickCounter


class TestClickCounter(unittest.TestCase):
    """Test cases for the ClickCounter class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.counter = ClickCounter()
        
        # Sample test data
        self.sample_encodes = [
            {"long_url": "https://google.com", "short_domain": "bit.ly", "hash": "a1b2c3"},
            {"long_url": "https://twitter.com", "short_domain": "bit.ly", "hash": "d4e5f6"},
            {"long_url": "https://example.com", "short_domain": "bit.ly", "hash": "g7h8i9"}
        ]
        
        self.sample_decodes = [
            {
                "bitlink": "http://bit.ly/a1b2c3",
                "timestamp": "2021-03-15T10:30:00+00:00",
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.1"
            },
            {
                "bitlink": "http://bit.ly/a1b2c3",
                "timestamp": "2021-04-15T10:30:00+00:00",
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.2"
            },
            {
                "bitlink": "http://bit.ly/d4e5f6",
                "timestamp": "2021-05-15T10:30:00+00:00",
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.3"
            },
            {
                "bitlink": "http://bit.ly/g7h8i9",
                "timestamp": "2020-12-31T10:30:00+00:00",  # Not 2021
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.4"
            },
            {
                "bitlink": "http://bit.ly/g7h8i9",
                "timestamp": "2022-01-01T10:30:00+00:00",  # Not 2021
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.5"
            }
        ]
    
    def test_parse_encodes_valid_file(self):
        """Test parsing a valid encodes CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain', 'hash'])
            writer.writeheader()
            writer.writerows(self.sample_encodes)
            temp_file = f.name
        
        try:
            counter = ClickCounter(temp_file, "dummy.json")
            result = counter.parse_encodes()
            
            expected = {
                "a1b2c3": "https://google.com",
                "d4e5f6": "https://twitter.com",
                "g7h8i9": "https://example.com"
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(counter.hash_to_url, expected)
        finally:
            os.unlink(temp_file)
    
    def test_parse_encodes_file_not_found(self):
        """Test parsing when encodes file doesn't exist."""
        counter = ClickCounter("nonexistent.csv", "dummy.json")
        
        with self.assertRaises(FileNotFoundError):
            counter.parse_encodes()
    
    def test_parse_encodes_missing_columns(self):
        """Test parsing when required columns are missing."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain'])  # Missing 'hash'
            writer.writeheader()
            writer.writerow({"long_url": "https://example.com", "short_domain": "bit.ly"})
            temp_file = f.name
        
        try:
            counter = ClickCounter(temp_file, "dummy.json")
            
            with self.assertRaises(ValueError):
                counter.parse_encodes()
        finally:
            os.unlink(temp_file)
    
    def test_parse_encodes_empty_values(self):
        """Test parsing with empty hash or URL values."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain', 'hash'])
            writer.writeheader()
            writer.writerow({"long_url": "https://example.com", "short_domain": "bit.ly", "hash": ""})
            writer.writerow({"long_url": "", "short_domain": "bit.ly", "hash": "abc123"})
            writer.writerow({"long_url": "https://valid.com", "short_domain": "bit.ly", "hash": "def456"})
            temp_file = f.name
        
        try:
            counter = ClickCounter(temp_file, "dummy.json")
            result = counter.parse_encodes()
            
            # Should only include the valid row
            expected = {"def456": "https://valid.com"}
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file)
    
    def test_parse_decodes_valid_file(self):
        """Test parsing a valid decodes JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.sample_decodes, f)
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            result = counter.parse_decodes()
            
            # Should only include 2021 events
            expected = ["a1b2c3", "a1b2c3", "d4e5f6"]
            self.assertEqual(result, expected)
            self.assertEqual(counter.click_events, expected)
        finally:
            os.unlink(temp_file)
    
    def test_parse_decodes_file_not_found(self):
        """Test parsing when decodes file doesn't exist."""
        counter = ClickCounter("dummy.csv", "nonexistent.json")
        
        with self.assertRaises(FileNotFoundError):
            counter.parse_decodes()
    
    def test_parse_decodes_invalid_json(self):
        """Test parsing with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            
            with self.assertRaises(ValueError):
                counter.parse_decodes()
        finally:
            os.unlink(temp_file)
    
    def test_parse_decodes_not_array(self):
        """Test parsing when JSON is not an array."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"not": "an array"}, f)
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            
            with self.assertRaises(ValueError):
                counter.parse_decodes()
        finally:
            os.unlink(temp_file)
    
    def test_parse_decodes_missing_fields(self):
        """Test parsing with missing required fields."""
        invalid_decodes = [
            {"bitlink": "http://bit.ly/a1b2c3"},  # Missing timestamp
            {"timestamp": "2021-03-15T10:30:00+00:00"},  # Missing bitlink
            {"bitlink": "http://bit.ly/d4e5f6", "timestamp": "invalid_timestamp"}  # Invalid timestamp
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(invalid_decodes, f)
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            result = counter.parse_decodes()
            
            # Should return empty list due to invalid data
            self.assertEqual(result, [])
        finally:
            os.unlink(temp_file)
    
    def test_count_clicks(self):
        """Test counting clicks functionality."""
        counter = ClickCounter()
        counter.click_events = ["a1b2c3", "a1b2c3", "d4e5f6", "a1b2c3", "g7h8i9"]
        
        result = counter.count_clicks()
        
        expected = {"a1b2c3": 3, "d4e5f6": 1, "g7h8i9": 1}
        self.assertEqual(result, expected)
    
    def test_count_clicks_empty(self):
        """Test counting clicks with no events."""
        counter = ClickCounter()
        counter.click_events = []
        
        result = counter.count_clicks()
        
        self.assertEqual(result, {})
    
    def test_map_clicks_to_urls(self):
        """Test mapping clicks to URLs."""
        counter = ClickCounter()
        counter.hash_to_url = {
            "a1b2c3": "https://google.com",
            "d4e5f6": "https://twitter.com",
            "g7h8i9": "https://example.com"
        }
        
        click_counts = {"a1b2c3": 3, "d4e5f6": 2, "xyz789": 1}  # xyz789 not in mapping
        
        result = counter.map_clicks_to_urls(click_counts)
        
        expected = [
            {"https://google.com": 3},
            {"https://twitter.com": 2}
        ]
        self.assertEqual(result, expected)
    
    def test_map_clicks_to_urls_no_matches(self):
        """Test mapping when no hashes match."""
        counter = ClickCounter()
        counter.hash_to_url = {"a1b2c3": "https://google.com"}
        
        click_counts = {"xyz789": 5}
        
        result = counter.map_clicks_to_urls(click_counts)
        
        self.assertEqual(result, [])
    
    def test_sort_results(self):
        """Test sorting results by click count."""
        counter = ClickCounter()
        
        url_clicks = [
            {"https://example.com": 1},
            {"https://google.com": 5},
            {"https://twitter.com": 3}
        ]
        
        result = counter.sort_results(url_clicks)
        
        expected = [
            {"https://google.com": 5},
            {"https://twitter.com": 3},
            {"https://example.com": 1}
        ]
        self.assertEqual(result, expected)
    
    def test_sort_results_same_counts(self):
        """Test sorting when some URLs have the same click count."""
        counter = ClickCounter()
        
        url_clicks = [
            {"https://example.com": 3},
            {"https://google.com": 3},
            {"https://twitter.com": 1}
        ]
        
        result = counter.sort_results(url_clicks)
        
        # Should maintain relative order for equal counts
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], {"https://example.com": 3})
        self.assertEqual(result[1], {"https://google.com": 3})
        self.assertEqual(result[2], {"https://twitter.com": 1})
    
    def test_process_integration(self):
        """Test the complete processing workflow."""
        # Create temporary files with test data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain', 'hash'])
            writer.writeheader()
            writer.writerows(self.sample_encodes)
            encodes_file = f.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.sample_decodes, f)
            decodes_file = f.name
        
        try:
            counter = ClickCounter(encodes_file, decodes_file)
            result = counter.process()
            
            # Expected result based on test data:
            # a1b2c3 (google.com) has 2 clicks
            # d4e5f6 (twitter.com) has 1 click
            expected = [
                {"https://google.com": 2},
                {"https://twitter.com": 1}
            ]
            
            self.assertEqual(result, expected)
        finally:
            os.unlink(encodes_file)
            os.unlink(decodes_file)
    
    def test_process_file_not_found(self):
        """Test process method when files don't exist."""
        counter = ClickCounter("nonexistent.csv", "nonexistent.json")
        
        with self.assertRaises(FileNotFoundError):
            counter.process()


class TestClickCounterEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_encodes_file(self):
        """Test with empty encodes file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain', 'hash'])
            writer.writeheader()
            # No data rows
            temp_file = f.name
        
        try:
            counter = ClickCounter(temp_file, "dummy.json")
            result = counter.parse_encodes()
            
            self.assertEqual(result, {})
        finally:
            os.unlink(temp_file)
    
    def test_empty_decodes_file(self):
        """Test with empty decodes file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            result = counter.parse_decodes()
            
            self.assertEqual(result, [])
        finally:
            os.unlink(temp_file)
    
    def test_duplicate_hashes_in_encodes(self):
        """Test handling of duplicate hashes in encodes file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            writer = csv.DictWriter(f, fieldnames=['long_url', 'short_domain', 'hash'])
            writer.writeheader()
            writer.writerow({"long_url": "https://example1.com", "short_domain": "bit.ly", "hash": "abc123"})
            writer.writerow({"long_url": "https://example2.com", "short_domain": "bit.ly", "hash": "abc123"})
            temp_file = f.name
        
        try:
            counter = ClickCounter(temp_file, "dummy.json")
            result = counter.parse_encodes()
            
            # Should contain the last occurrence
            expected = {"abc123": "https://example2.com"}
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file)
    
    def test_timestamp_edge_cases(self):
        """Test various timestamp formats and edge cases."""
        edge_case_decodes = [
            {
                "bitlink": "http://bit.ly/a1b2c3",
                "timestamp": "2021-01-01T00:00:00+00:00",  # Start of 2021
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.1"
            },
            {
                "bitlink": "http://bit.ly/d4e5f6",
                "timestamp": "2021-12-31T23:59:59+00:00",  # End of 2021
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.2"
            },
            {
                "bitlink": "http://bit.ly/g7h8i9",
                "timestamp": "2021-06-15T12:00:00Z",  # Z format
                "user_agent": "Mozilla/5.0",
                "ip_address": "192.168.1.3"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(edge_case_decodes, f)
            temp_file = f.name
        
        try:
            counter = ClickCounter("dummy.csv", temp_file)
            result = counter.parse_decodes()
            
            # All should be included as they're all from 2021
            expected = ["a1b2c3", "d4e5f6", "g7h8i9"]
            self.assertEqual(result, expected)
        finally:
            os.unlink(temp_file)


if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)
