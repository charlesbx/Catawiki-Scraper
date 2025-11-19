# 🔍 Catawiki Watch Auction Scraper

> **A sophisticated, production-ready real-time auction monitoring system for luxury watches on Catawiki.com**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Overview

This project is an intelligent web scraping and monitoring system that continuously tracks luxury watch auctions on Catawiki.com, identifies undervalued items based on estimated market prices, and sends real-time Telegram notifications when lucrative deals are found.

**Perfect for:** Collectors, dealers, and investors looking to acquire luxury watches below market value through automated monitoring.

### Key Features

🎯 **Smart Deal Detection**
- Real-time price monitoring against estimated market values
- Configurable threshold-based filtering (default: items priced ≤90% of estimate)
- Reserve price status tracking
- Time-sensitive opportunity identification

🤖 **Intelligent Scraping**
- Automatic pagination and infinite scroll handling
- Robust retry logic with exponential backoff
- Rate limiting to respect target site
- Headless browser support for efficiency

📱 **Real-time Notifications**
- Instant Telegram alerts for new deals
- Price update notifications
- Auction closing warnings
- Multi-recipient support

🔒 **Production-Ready**
- Environment-based configuration
- Comprehensive error handling
- Structured logging
- Type-safe code with full type hints

## 🏗️ Architecture

```
┌─────────────────┐
│   Catawiki.com  │
│   (Watch Page)  │
└────────┬────────┘
         │ HTTP/Selenium
         ▼
┌─────────────────┐
│  Web Scraper    │◄── BeautifulSoup + Selenium
│  (Browser Auto) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Data Parser    │◄── Extract & normalize listings
│  & Validator    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Deal Analyzer  │◄── Filter by price/time thresholds
│  & Filter       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  JSON Storage   │◄── Persistent local database
│  (items.json)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Telegram Bot   │◄── Send notifications
│  (python-telegram-bot)
└─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Chrome/Chromium browser
- ChromeDriver (matching your browser version)
- Telegram bot token (from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/charlesbx/Catawiki-Scraper.git
   cd Catawiki-Scraper
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Set up your Telegram bot**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Copy the bot token to `.env`
   - Start a chat with your bot and get your chat ID
   - Add chat ID(s) to `.env`

### Configuration

Edit `.env` file with your settings:

```bash
# Required: Telegram credentials
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_IDS=123456789,987654321

# Optional: Scraper settings
PRICE_PERCENTAGE_THRESHOLD=0.90  # Alert for items ≤90% of estimate
REMAINING_TIME_THRESHOLD=1800     # Alert when <30min remaining
SCRAPER_MAX_ITEMS=300            # Max items to scrape per run
HEADLESS_MODE=true               # Run browser in background
```

### Usage

**Scrape current listings:**
```bash
python main.py
```

**Monitor for deals (single check):**
```bash
python load.py
```

**Continuous monitoring:**
```bash
python checkItemLoop.py
```

**Extract and notify on good offers:**
```bash
python extract_good_offer.py
```

## 📊 Features in Detail

### Deal Detection Algorithm

The system uses a multi-factor approach to identify valuable opportunities:

1. **Price Analysis**
   - Compares current bid against median estimated value
   - Default threshold: 90% (configurable)
   - Example: €5,000 bid on item estimated €7,000-€9,000 → Alert! (62.5% of median)

2. **Time Sensitivity**
   - Tracks remaining auction time
   - Prioritizes items closing soon
   - Sends urgent notifications for <30min remaining

3. **Reserve Price Status**
   - Filters out items with unmet reserves
   - Focuses on actionable opportunities
   - Tracks status changes

### Notification System

Telegram messages include:
- Item title and reference
- Current price vs estimated range
- Time remaining (dynamically updated)
- Direct auction URL
- Reserve price status

**Message Types:**
- 🆕 **NEW OFFER FOUND** - New deal detected
- 🔄 **OFFER UPDATED** - Price/status change
- ⏰ **CLOSING SOON** - <90s remaining

## 🛠️ Technology Stack

- **Python 3.10+** - Modern async/await patterns
- **Selenium 4.x** - Browser automation
- **BeautifulSoup4** - HTML parsing
- **python-telegram-bot** - Telegram API client
- **python-dotenv** - Environment management
- **Type hints** - Full type safety

## 📁 Project Structure

```
catawiki-scraper/
├── config.py              # Configuration management
├── utils.py               # Time parsing utilities
├── main.py                # Core scraping logic
├── load.py                # Deal loading & display
├── checkItem.py           # Single item check
├── checkItemLoop.py       # Continuous monitoring
├── extract_good_offer.py  # Deal extraction & notification
├── SendTelegramMessage.py # Telegram client
├── items.json             # Scraped data (auto-generated)
├── requirements.txt       # Python dependencies
├── .env.example           # Configuration template
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔐 Security

- ✅ No hardcoded credentials
- ✅ Environment variable configuration
- ✅ `.env` excluded from version control
- ✅ Secure token handling
- ⚠️ **Important:** Never commit your `.env` file

## 🎯 Why This Project Demonstrates Strong Engineering

### 1. **Real-World Problem Solving**
- Addresses actual market inefficiency (information asymmetry)
- Provides tangible value to users
- Operates in production environment

### 2. **Technical Complexity**
- Dynamic content scraping (infinite scroll, AJAX)
- Robust error handling and retry logic
- Real-time monitoring with state management
- Multi-channel notifications

### 3. **Best Practices**
- Clean, modular architecture
- Type-safe code with full type hints
- Environment-based configuration
- Comprehensive documentation

### 4. **Production Readiness**
- Automated monitoring capabilities
- Error recovery and logging
- Scalable design patterns
- Security-conscious implementation

## 📈 Future Enhancements

Potential improvements showcase scalability thinking:

- [ ] Database backend (PostgreSQL/SQLite)
- [ ] RESTful API for remote access
- [ ] Web dashboard for monitoring
- [ ] Machine learning for price prediction
- [ ] Multi-site support (other auction platforms)
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Comprehensive test suite

## 🤝 Contributing

This is a portfolio project, but suggestions and feedback are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for:
- Complying with Catawiki's Terms of Service
- Respecting robots.txt and rate limits
- Using scraped data ethically and legally

**Note:** Automated scraping may violate terms of service. Use responsibly.

## 👤 Author

**Charles Baux**
- GitHub: [@charlesbx](https://github.com/charlesbx)
- Portfolio: [Your Portfolio URL]

## 🙏 Acknowledgments

- Catawiki.com for providing the auction platform
- Python community for excellent libraries
- Telegram for their bot API

---

**⭐ If you find this project interesting, please star the repository!**
