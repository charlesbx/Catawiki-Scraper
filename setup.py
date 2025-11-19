#!/usr/bin/env python3
"""
Setup script for Catawiki Scraper.
Handles initial configuration and environment setup.
"""
import os
import sys
import shutil
from pathlib import Path


def print_header(text: str) -> None:
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def check_python_version() -> bool:
    """Check if Python version is 3.10+."""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10 or higher is required!")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_chrome() -> bool:
    """Check if Chrome/Chromium is installed."""
    chrome_paths = [
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/bin/google-chrome",
        "/usr/bin/chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome/Chromium found: {path}")
            return True
    
    print("⚠️  Chrome/Chromium not found in standard locations")
    print("   Please install Chrome or update CHROME_BINARY in .env")
    return False


def setup_env_file() -> bool:
    """Create .env from .env.example if it doesn't exist."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example not found!")
        return False
    
    try:
        shutil.copy(env_example, env_file)
        print("✅ Created .env from .env.example")
        print("   ⚠️  Please edit .env with your Telegram credentials!")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env: {e}")
        return False


def create_directories() -> None:
    """Create necessary directories."""
    dirs = ["logs", "data"]
    
    for dir_name in dirs:
        path = Path(dir_name)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Created directory: {dir_name}/")


def check_dependencies() -> bool:
    """Check if required packages can be imported."""
    required = [
        ("selenium", "Selenium"),
        ("bs4", "BeautifulSoup4"),
        ("telegram", "python-telegram-bot"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing = []
    for module, package in required:
        try:
            __import__(module)
            print(f"✅ {package} installed")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} not found")
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True


def print_next_steps() -> None:
    """Print next steps for the user."""
    print_header("Setup Complete!")
    
    print("📝 Next Steps:\n")
    print("1. Edit .env file with your Telegram credentials:")
    print("   - Get bot token from @BotFather on Telegram")
    print("   - Get your chat ID (use @userinfobot)")
    print()
    print("2. Install dependencies (if not already done):")
    print("   pip install -r requirements.txt")
    print()
    print("3. Run a test scrape:")
    print("   python main.py")
    print()
    print("4. Monitor for deals:")
    print("   python extract_good_offer.py")
    print()
    print("📚 Documentation:")
    print("   - README.md - Project overview")
    print("   - docs/ARCHITECTURE.md - Architecture details")
    print()
    print("⚠️  Important: Never commit your .env file!")
    print()


def main():
    """Main setup function."""
    print_header("Catawiki Scraper Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Chrome
    check_chrome()
    
    # Setup .env
    if not setup_env_file():
        print("\n⚠️  Please create .env file manually from .env.example")
    
    # Create directories
    create_directories()
    
    # Check dependencies
    print("\n" + "="*60)
    print("Checking Dependencies...")
    print("="*60 + "\n")
    deps_ok = check_dependencies()
    
    # Print next steps
    print_next_steps()
    
    if not deps_ok:
        print("⚠️  Please install missing dependencies before running!")
        sys.exit(1)


if __name__ == "__main__":
    main()
