# Bitly Backend Engineer Coding Challenge Solution

This repository contains a Python solution for the Bitly Backend Engineer Coding Challenge. The solution calculates the number of clicks from 2021 for each record in the encodes.csv dataset using click event data from decodes.json.

## Problem Statement

Using the click event data in `decodes.json`, calculate the number of clicks from 2021 for each record in the `encodes.csv` dataset.

**Expected Output**: A sorted array of JSON objects containing the long URL as the key and the click count as the value, sorted descending by click count.

Example:
```json
[
  {"https://google.com": 3},
  {"https://www.twitter.com": 2}
]
```

## Solution Overview

The solution implements a `ClickCounter` class that:

1. **Parses encodes.csv**: Creates a mapping of hash → long_url
2. **Parses decodes.json**: Extracts click events from 2021
3. **Counts clicks**: Aggregates click counts per hash for 2021
4. **Maps to URLs**: Associates click counts with their corresponding long URLs
5. **Sorts results**: Orders results by click count (descending)

## Dependencies

**No external dependencies required!** This solution uses only Python standard library modules:

- `csv`: For parsing CSV files
- `json`: For parsing JSON files  
- `logging`: For structured logging
- `collections.defaultdict`: For efficient counting
- `datetime`: For timestamp parsing
- `typing`: For type hints
- `sys`, `os`: For system operations
- `unittest`: For unit testing
- `tempfile`: For creating temporary test files

### Python Version

- **Recommended**: Python 3.7 or higher
- **Minimum**: Python 3.6 (for f-string support)

## Installation

Since no external dependencies are required, installation is straightforward:

1. **Clone or download** this repository
2. **Ensure Python 3.7+** is installed on your system
3. **Verify Python installation**:
   ```bash
   python --version
   # or
   python3 --version
   ```

## Usage

### Running the Application

1. **Place your data files** in the project directory:
   - `encodes.csv`: Contains long_url, short_domain, hash columns
   - `decodes.json`: Contains click event data with timestamps

2. **Run the main script**:
   ```bash
   python click_counter.py
   # or
   python3 click_counter.py
   ```

3. **Expected output**: JSON array printed to console with sorted results

### Running Unit Tests

```bash
python test_click_counter.py
# or
python3 test_click_counter.py
```

For verbose test output:
```bash
python test_click_counter.py -v
```

### Using with Custom File Paths

```python
from click_counter import ClickCounter

# Initialize with custom file paths
counter = ClickCounter("path/to/encodes.csv", "path/to/decodes.json")

# Process the data
results = counter.process()

# Print results
import json
print(json.dumps(results, indent=2))
```

## Data Format Requirements

### encodes.csv
```csv
long_url,short_domain,hash
https://google.com,bit.ly,a1b2c3
https://twitter.com,bit.ly,d4e5f6
```

### decodes.json
```json
[
  {
    "bitlink_hash": "a1b2c3",
    "timestamp": "2021-03-15T10:30:00+00:00",
    "user_agent": "Mozilla/5.0...",
    "ip_address": "192.168.1.1"
  }
]
```

## Design Decisions

### 1. Object-Oriented Approach
- **Decision**: Used a `ClickCounter` class to encapsulate functionality
- **Rationale**: Provides better organization, testability, and maintainability
- **Benefits**: Clear separation of concerns, reusable components

### 2. Comprehensive Error Handling
- **Decision**: Added extensive error handling and logging throughout
- **Rationale**: Production-ready code should handle edge cases gracefully
- **Benefits**: Better debugging, robust operation, informative error messages

### 3. Type Hints
- **Decision**: Added comprehensive type hints to all methods
- **Rationale**: Improves code clarity and enables better IDE support
- **Benefits**: Better documentation, easier maintenance, fewer runtime errors

### 4. Structured Logging
- **Decision**: Implemented detailed logging at INFO, WARNING, and ERROR levels
- **Rationale**: Essential for monitoring and debugging in production environments
- **Benefits**: Better observability, easier troubleshooting

### 5. Comprehensive Testing
- **Decision**: Created extensive unit tests covering all functions and edge cases
- **Rationale**: Ensures reliability and catches regressions
- **Benefits**: High confidence in correctness, easier refactoring

### 6. Memory Efficiency
- **Decision**: Process data in streaming fashion where possible
- **Rationale**: Handle large datasets without memory issues
- **Benefits**: Scalable to larger datasets

### 7. Input Validation
- **Decision**: Validate file existence, format, and required fields
- **Rationale**: Fail fast with clear error messages
- **Benefits**: Better user experience, easier debugging

## File Structure

```
bitly-challenge/
├── click_counter.py          # Main solution implementation
├── test_click_counter.py     # Comprehensive unit tests
├── encodes.csv              # Sample encodes data (hash → URL mapping)
├── decodes.json             # Sample decodes data (click events)
├── requirements.txt         # Dependencies (none required)
├── README.md               # This documentation
├── ai_usage.md             # AI tool usage documentation
└── Dockerfile              # Container configuration (optional)
```

## Testing

The solution includes comprehensive unit tests that cover:

- **Valid data processing**: Normal operation with correct input
- **File not found errors**: Missing input files
- **Invalid data formats**: Malformed CSV/JSON
- **Missing required fields**: Incomplete data records
- **Edge cases**: Empty files, duplicate hashes, timestamp boundaries
- **Integration testing**: End-to-end workflow validation

Run tests with:
```bash
python test_click_counter.py -v
```

## Logging

The application provides detailed logging at multiple levels:

- **INFO**: Normal operation progress (file parsing, counts, sorting)
- **WARNING**: Non-fatal issues (missing fields, unmatched hashes)
- **ERROR**: Fatal errors (file not found, invalid format)

Example log output:
```
2024-01-15 10:30:00,123 - INFO - Starting click counting process
2024-01-15 10:30:00,124 - INFO - Parsing encodes file: encodes.csv
2024-01-15 10:30:00,125 - INFO - Successfully parsed 1000 rows from encodes file
2024-01-15 10:30:00,126 - INFO - Parsing decodes file: decodes.json
2024-01-15 10:30:00,127 - INFO - Found 500 click events from 2021
```

## Performance Considerations

- **Time Complexity**: O(n log n) due to sorting step
- **Space Complexity**: O(n) for storing hash mappings and click counts
- **Memory Usage**: Efficient streaming processing for large files
- **Scalability**: Can handle datasets with millions of records

## Error Handling

The solution handles various error conditions:

1. **File not found**: Clear error message with file path
2. **Invalid CSV format**: Missing columns, malformed rows
3. **Invalid JSON format**: Syntax errors, wrong data types
4. **Missing required fields**: bitlink_hash, timestamp
5. **Invalid timestamps**: Unparseable date formats
6. **Empty files**: Graceful handling of empty input

## Future Enhancements

Potential improvements for production use:

1. **Command-line interface**: Add argparse for file path options
2. **Configuration file**: Support for configurable date ranges
3. **Database integration**: Replace file I/O with database queries
4. **API endpoints**: REST API for real-time processing
5. **Caching**: Redis/memcached for frequently accessed data
6. **Monitoring**: Metrics collection and alerting
7. **Batch processing**: Support for multiple file processing

## Troubleshooting

### Common Issues

1. **"File not found" error**
   - Ensure `encodes.csv` and `decodes.json` exist in the current directory
   - Check file permissions

2. **"Missing required columns" error**
   - Verify CSV has `long_url`, `short_domain`, `hash` columns
   - Check for typos in column headers

3. **"Invalid JSON" error**
   - Validate JSON syntax using online JSON validator
   - Ensure file contains a JSON array

4. **No output**
   - Check that decodes.json contains events from 2021
   - Verify timestamp format matches ISO 8601 with timezone

### Debug Mode

For additional debugging information, modify the logging level:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## License

This solution is provided as part of the Bitly Backend Engineer Coding Challenge submission.
