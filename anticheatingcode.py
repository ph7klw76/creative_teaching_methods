import os
import glob
from difflib import SequenceMatcher
from itertools import combinations

def get_similarity(text1, text2):
    """Calculates the similarity ratio between two texts."""
    return SequenceMatcher(None, text1, text2).ratio()

def check_directory_similarity(folder_path, threshold=0.90):
    """
    Scans a directory for .py files and prints a table of pairs 
    with similarity greater than the threshold.
    """
    # 1. Gather all Python files
    # Using 'recursive=True' and '**' lets you search subdirectories if needed
    # For now, we search just the top-level folder provided.
    py_files = glob.glob(os.path.join(folder_path, "*.py"))

    if len(py_files) < 2:
        print("Not enough Python files found to compare.")
        return

    print(f"Found {len(py_files)} Python files. Processing...")

    # 2. Read file contents into memory
    file_contents = {}
    for file_path in py_files:
        filename = os.path.basename(file_path)
        try:
            # errors='ignore' prevents crashing on non-utf-8 files
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                file_contents[filename] = f.read()
        except Exception as e:
            print(f"Skipping {filename}: {e}")

    # 3. Compare every unique pair
    # itertools.combinations('ABCD', 2) --> AB AC AD BC BD CD
    pairs = combinations(file_contents.keys(), 2)
    
    matches = []

    for name1, name2 in pairs:
        content1 = file_contents[name1]
        content2 = file_contents[name2]

        # Optimization: Skip if one file is empty to avoid skewing results
        if not content1 or not content2:
            continue

        similarity = get_similarity(content1, content2)

        if similarity > threshold:
            matches.append((name1, name2, similarity))

    # 4. Print results in a table format
    if matches:
        # Sort matches by highest similarity first
        matches.sort(key=lambda x: x[2], reverse=True)

        print("\n" + "="*80)
        print(f"{'File A':<35} | {'File B':<35} | {'Similarity'}")
        print("-" * 80)
        
        for file_a, file_b, score in matches:
            # Truncate filenames if they are too long for the table
            fa_display = (file_a[:32] + '..') if len(file_a) > 34 else file_a
            fb_display = (file_b[:32] + '..') if len(file_b) > 34 else file_b
            
            # Print row
            print(f"{fa_display:<35} | {fb_display:<35} | {score*100:.2f}%")
        print("="*80 + "\n")
    else:
        print("\nNo files found with similarity above 90%.\n")

if __name__ == "__main__":
    # You can hardcode the path here or take user input
    target_dir = input("Enter the directory path containing Python files: ").strip()
    
    if os.path.isdir(target_dir):
        check_directory_similarity(target_dir)
    else:
        print("Invalid directory path.")
