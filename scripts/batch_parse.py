import argparse
import logging
from pathlib import Path
from parse_tcu_data import run_script

def find_logs_folders(root_folder):
    """Find all LOGS folders in the root directory"""
    logs_folders = []
    root_path = Path(root_folder)
    
    for item in root_path.iterdir():
        if item.is_dir() and item.name.startswith('LOGS'):
            logs_folders.append(item)
    
    return sorted(logs_folders)

def find_txt_files(logs_folder):
    """Find all txt files in a LOGS folder"""
    txt_files = []
    logs_path = Path(logs_folder)
    
    for item in logs_path.iterdir():
        if item.is_file() and item.suffix.lower() == '.txt':
            txt_files.append(item)
    
    return txt_files

def main():
    parser = argparse.ArgumentParser(description="Batch process CAN log folders using TCU data parser")
    parser.add_argument('root_folder', help="Root folder containing LOGS folders")
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')
    
    # Validate root folder
    root_path = Path(args.root_folder)
    if not root_path.exists() or not root_path.is_dir():
        logging.error(f"Root folder does not exist: {args.root_folder}")
        return
    
    # Find all LOGS folders
    logs_folders = find_logs_folders(args.root_folder)
    if not logs_folders:
        logging.error("No LOGS folders found in the root directory")
        return
    
    logging.info(f"Found {len(logs_folders)} LOGS folders")
    
    # Process each LOGS folder
    total_files_processed = 0
    for logs_folder in logs_folders:
        logging.info(f"Processing folder: {logs_folder.name}")
        
        # Find txt files in this LOGS folder
        txt_files = find_txt_files(logs_folder)
        if not txt_files:
            logging.warning(f"No txt files found in {logs_folder.name}")
            continue
        
        # Process each txt file
        for txt_file in txt_files:
            logging.debug(f"Processing file: {txt_file.name}")
            
            try:
                # Use the run_script function from parse_tcu_data.py
                # Pass the root folder as the first argument to maintain directory structure
                run_script(root_path, txt_file)
                logging.debug(f"Successfully processed: {txt_file}")
                total_files_processed += 1
            except Exception as e:
                logging.error(f"Error processing {txt_file}: {e}")
    
    logging.info(f"Batch processing completed. {total_files_processed} files processed.")
    logging.info(f"Output written to: {Path('parsed_files')}")

if __name__ == "__main__":
    main()