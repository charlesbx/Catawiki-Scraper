# 🏗️ Architecture Documentation

## Overview

The Catawiki Scraper follows a **modular, layered architecture** designed for maintainability, testability, and scalability. The system is organized into distinct modules with clear responsibilities and minimal coupling.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Entry Points (scripts/)                  │
│  scrape_listings.py | monitor_deals.py | check_items.py    │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                   Application Layer                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │   Scraper    │  │   Analyzer   │  │ Notification │    │
│  │   Module     │──│   Module     │──│   Module     │    │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘    │
│         │                  │                  │             │
│         │                  │                  │             │
│  ┌──────▼──────────────────▼──────────────────▼───────┐   │
│  │           Storage & Data Models                     │   │
│  │        (JSON Store, WatchItem, DealAlert)           │   │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Utilities (Logger, Time Utils, Config)        │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────┐
│                  External Services                           │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  Catawiki    │  │   Telegram   │  │  File System │    │
│  │  Website     │  │     Bot      │  │  (JSON/Logs) │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
catawiki-scraper/
├── src/                          # Source code modules
│   ├── __init__.py
│   ├── scraper/                  # Web scraping logic
│   │   ├── __init__.py
│   │   ├── browser.py            # Browser management
│   │   ├── parser.py             # HTML parsing (TODO)
│   │   └── watch_scraper.py      # Main scraping logic (TODO)
│   ├── analyzer/                 # Deal analysis
│   │   ├── __init__.py
│   │   └── filters.py            # Deal filtering & scoring
│   ├── notifications/            # Alert system
│   │   ├── __init__.py
│   │   └── telegram.py           # Telegram client
│   ├── storage/                  # Data persistence
│   │   ├── __init__.py
│   │   ├── json_store.py         # JSON file operations
│   │   └── models.py             # Data models (WatchItem, etc.)
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   └── settings.py           # Environment-based config
│   └── utils/                    # Utilities
│       ├── __init__.py
│       ├── logger.py             # Logging setup
│       └── time_utils.py         # Time parsing functions
├── scripts/                      # Entry point scripts
│   ├── scrape_listings.py        # Initial scraping
│   ├── monitor_deals.py          # Continuous monitoring
│   └── check_items.py            # Item verification
├── tests/                        # Test suite
│   ├── test_analyzer.py
│   ├── test_scraper.py
│   └── ...
├── docs/                         # Documentation
│   ├── ARCHITECTURE.md           # This file
│   └── API.md                    # API documentation
├── config.py                     # Legacy config (deprecated)
├── main.py                       # Legacy main (deprecated)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview
```

## Module Responsibilities

### 1. Scraper Module (`src/scraper/`)

**Purpose:** Handle all web scraping operations.

**Components:**
- `browser.py`: Manages Chrome/Chromium browser instances
  - Configuration (headless, user agent, etc.)
  - Driver lifecycle management
  - Context manager support
  
- `parser.py` (TODO): HTML parsing and data extraction
  - BeautifulSoup integration
  - CSS selector definitions
  - Data normalization

- `watch_scraper.py` (TODO): Main scraping orchestration
  - Pagination handling
  - Infinite scroll
  - Item extraction pipeline

**Key Design Decisions:**
- Separation of browser management from parsing logic
- Context manager pattern for resource cleanup
- Configurable browser options via environment

### 2. Analyzer Module (`src/analyzer/`)

**Purpose:** Analyze items to identify good deals.

**Components:**
- `filters.py`: Deal detection and scoring
  - `DealCriteria`: Configurable filtering thresholds
  - `DealAnalyzer`: Main analysis engine
  - Price ratio calculations
  - Time-based urgency detection
  - Deal quality scoring

**Key Features:**
- Configurable thresholds (price %, time remaining)
- Reserve price filtering
- Multiple filtering strategies
- Deal quality scoring (0.0 = best, 1.0 = worst)

### 3. Notifications Module (`src/notifications/`)

**Purpose:** Send alerts to users.

**Components:**
- `telegram.py`: Telegram Bot API integration
  - Async message sending
  - Multi-recipient support
  - Error handling per recipient

**Design Patterns:**
- Async/await for non-blocking I/O
- Graceful degradation (continues if one recipient fails)

### 4. Storage Module (`src/storage/`)

**Purpose:** Data persistence and models.

**Components:**
- `models.py`: Data classes
  - `WatchItem`: Represents auction listing
  - `DealAlert`: Notification representation
  - Helper methods for price parsing
  
- `json_store.py`: JSON file operations
  - CRUD operations
  - Automatic backups
  - URL-based lookups
  - Safe file operations

**Key Features:**
- Dataclass-based models (immutable, type-safe)
- Automatic backup before write
- URL-based indexing
- Type-safe conversions (to_dict, from_dict)

### 5. Config Module (`src/config/`)

**Purpose:** Centralized configuration management.

**Components:**
- `settings.py`: Environment-based config
  - Loads from `.env` file
  - Type conversions (str → int, float, bool)
  - Validation of required values
  - Default values for optional settings

**Configuration Sources:**
1. `.env` file (primary)
2. Environment variables
3. Hardcoded defaults (fallback)

### 6. Utils Module (`src/utils/`)

**Purpose:** Shared utilities across modules.

**Components:**
- `logger.py`: Logging configuration
  - Console + file handlers
  - Configurable log levels
  - Structured formatting
  
- `time_utils.py`: Time parsing
  - French time format parsing (1j 5h 30m)
  - Remaining time calculations
  - Seconds ↔ human-readable conversion

## Data Flow

### 1. Scraping Flow

```
User runs script
    ↓
BrowserManager creates driver
    ↓
Scraper navigates to Catawiki
    ↓
Parser extracts item data
    ↓
WatchItem objects created
    ↓
JSONStorage saves items
    ↓
Browser closed
```

### 2. Deal Detection Flow

```
Load items from JSONStorage
    ↓
For each item:
    ↓
    DealAnalyzer.is_good_deal()
        ├─ Check price vs estimate
        ├─ Check remaining time
        └─ Check reserve status
    ↓
Filter good deals
    ↓
Sort by deal quality
    ↓
Return filtered list
```

### 3. Notification Flow

```
Good deals identified
    ↓
For each deal:
    ↓
    Format message
    ↓
    Create DealAlert
    ↓
    send_telegram_message()
        ├─ Send to recipient 1
        ├─ Send to recipient 2
        └─ ...
    ↓
Log success/failure
```

## Design Patterns

### 1. **Context Manager Pattern**
Used in `BrowserManager` for automatic resource cleanup:
```python
with BrowserManager() as driver:
    # Use driver
    pass
# Automatically closed
```

### 2. **Dataclass Pattern**
Used in `models.py` for type-safe, immutable data:
```python
@dataclass
class WatchItem:
    title: str
    price: str
    # ...
```

### 3. **Strategy Pattern**
`DealCriteria` allows different filtering strategies:
```python
criteria = DealCriteria(
    price_threshold=0.80,  # 80% instead of 90%
    time_threshold=3600    # 1 hour instead of 30min
)
analyzer = DealAnalyzer(criteria)
```

### 4. **Repository Pattern**
`JSONStorage` abstracts data access:
```python
storage = JSONStorage("items.json")
items = storage.load()
storage.save(updated_items)
```

## Error Handling Strategy

### 1. **Graceful Degradation**
- Telegram send failures don't stop other recipients
- Parser errors skip item, continue with next

### 2. **Logging**
- All errors logged with context
- Different log levels (DEBUG, INFO, WARNING, ERROR)

### 3. **Validation**
- Config validation on startup
- Data validation in models
- Type hints for compile-time checks

## Testing Strategy

### 1. **Unit Tests**
- Individual functions (e.g., `get_total_seconds`)
- Pure logic (no external dependencies)

### 2. **Integration Tests**
- Module interactions (e.g., DealAnalyzer + JSONStorage)
- Mocked external services

### 3. **E2E Tests**
- Full scraping pipeline (with mocked website)
- Notification flow

## Performance Considerations

### 1. **Browser Optimization**
- Headless mode reduces overhead
- Image loading disabled
- Minimal wait times

### 2. **Data Efficiency**
- JSON for fast read/write
- In-memory filtering (no DB overhead)
- Backup only when data changes

### 3. **Network**
- Rate limiting (TODO)
- Retry logic with backoff (TODO)
- Connection pooling (TODO)

## Security

### 1. **Credentials**
- Never committed to Git
- Environment variables only
- `.env` in `.gitignore`

### 2. **Input Validation**
- URL validation
- Price parsing with error handling
- Type checking everywhere

### 3. **Dependencies**
- Pinned versions in `requirements.txt`
- Regular security updates

## Future Enhancements

### 1. **Database Backend**
- Replace JSON with SQLite/PostgreSQL
- Indexed queries for performance
- Historical data tracking

### 2. **API Layer**
- RESTful API for remote access
- Authentication & authorization
- Rate limiting

### 3. **Distributed Architecture**
- Separate scraper, analyzer, notifier
- Message queue (RabbitMQ/Redis)
- Horizontal scaling

### 4. **Monitoring**
- Health checks
- Metrics (Prometheus)
- Dashboards (Grafana)

## Backward Compatibility

Legacy files maintained temporarily for migration:
- `config.py` → `src/config/settings.py`
- `utils.py` → `src/utils/time_utils.py`
- `main.py` → `scripts/scrape_listings.py`

**Deprecation Timeline:**
- **Phase 1** (Current): Both old and new coexist
- **Phase 2** (Next): Old files marked deprecated
- **Phase 3** (Future): Old files removed

---

**Document Version:** 2.0.0  
**Last Updated:** 2025-11-19  
**Maintainer:** Charles Baux
