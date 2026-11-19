import os
import shutil
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Define file categories and their corresponding extensions
FILE_CATEGORIES = {
    "Images": ['.jpeg', '.jpg', '.png', '.gif', '.bmp', '.svg', '.webp', '.tiff'],
    "Documents": ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.md', '.csv', '.xlsx', '.xls', '.pptx', '.ppt'],
    "Audio": ['.mp3', '.wav', '.aac', '.flac', '.ogg'],
    "Video": ['.mp4', '.avi', '.mkv', '.mov', '.wmv'],
    "Archives": ['.zip', '.tar', '.gz', '.rar', '.7z'],
    "Code": ['.py', '.js', '.html', '.css', '.cpp', '.java', '.json', '.sh', '.xml'],
    "Design": ['.psd', '.ai', '.fig', '.sketch'],
    "Executables": ['.exe', '.msi', '.apk', '.dmg', '.bat']
}

def get_category(extension: str) -> str:
    """Find the category for a given file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def get_unique_path(destination: Path, file_name: str) -> Path:
    """Ensure no files are overwritten by appending a counter to duplicates."""
    base_name = file_name.stem
    extension = file_name.suffix
    counter = 1
    
    new_path = destination / file_name.name
    while new_path.exists():
        new_path = destination / f"{base_name}_{counter}{extension}"
        counter += 1
        
    return new_path

def organize_directory(target_directory: str):
    """Organize files in the specified directory into categorized folders."""
    target_path = Path(target_directory).resolve()
    
    if not target_path.exists() or not target_path.is_dir():
        logging.error(f"The directory '{target_path}' does not exist or is not a directory.")
        return

    logging.info(f"Starting organization for: {target_path}")
    
    # Track statistics
    moved_files = 0
    skipped_files = 0

    for file_path in target_path.iterdir():
        # Skip directories and the script itself if it's in the same folder
        if file_path.is_dir() or file_path.name == Path(__file__).name:
            continue

        # Get file extension and determine category
        extension = file_path.suffix
        if not extension:
            # Handle files with no extension
            category = "Others"
        else:
            category = get_category(extension)

        # Create category directory if it doesn't exist
        category_dir = target_path / category
        category_dir.mkdir(exist_ok=True)

        # Generate a safe destination path to prevent overwriting
        dest_path = get_unique_path(category_dir, file_path)

        try:
            shutil.move(str(file_path), str(dest_path))
            logging.info(f"Moved: {file_path.name} -> {category}/{dest_path.name}")
            moved_files += 1
        except Exception as e:
            logging.error(f"Failed to move {file_path.name}: {e}")
            skipped_files += 1

    logging.info(f"Organization complete. Moved: {moved_files}, Skipped/Failed: {skipped_files}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by their extensions.")
    parser.add_argument(
        "directory", 
        nargs="?", 
        default=".", 
        help="Path to the directory you want to organize (defaults to current directory)"
    )
    
    args = parser.parse_args()
    organize_directory(args.directory)