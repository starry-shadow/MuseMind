import os
from datetime import datetime

def process_journal_entry(entry_text, response_text):
    # Get the absolute path to the journal entries directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    entry_dir = os.path.join(project_root, "MuseMind", "MuseMind", "Components", "wwwroot", "journal_entries")
    
    print(f"\n=== Processing journal files ===")
    print(f"Current directory: {current_dir}")
    print(f"Project root: {project_root}")
    print(f"Journal entries directory: {entry_dir}")
    
    if not os.path.exists(project_root):
        raise Exception(f"Project root directory not found: {project_root}")
    
    if not os.path.exists(os.path.join(project_root, "MuseMind")):
        raise Exception(f"MuseMind directory not found in: {project_root}")
    
    # Create all necessary directories
    os.makedirs(entry_dir, exist_ok=True)
    print(f"Created/verified journal entries directory")
    
    # Generate timestamp for the files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save the journal entry
    entry_file = os.path.join(entry_dir, f"{timestamp}_entry.txt")
    response_file = os.path.join(entry_dir, f"{timestamp}_response.txt")
    
    print(f"Saving entry to: {entry_file}")
    with open(entry_file, "w", encoding='utf-8') as f:
        f.write(entry_text)
    print(f"Entry file exists: {os.path.exists(entry_file)}")
        
    print(f"Saving response to: {response_file}")
    # Save the response
    with open(response_file, "w", encoding='utf-8') as f:
        f.write(response_text)
    print(f"Response file exists: {os.path.exists(response_file)}")
        
    return timestamp

if __name__ == "__main__":
    # For testing purposes
    test_entry = """Today I had so much work I feel anxious and overwhelmed with work and personal responsibilities. 
    I have trouble sleeping and concentrating. I often feel like I'm not good enough and worry about the future."""
    process_journal_entry(test_entry)