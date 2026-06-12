import os
from PIL import Image
import shutil

# Configuration
CASES_DIR = r"D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\cases"
OUTPUT_DIR = r"D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\cases_compressed"
MAX_SIZE = 1920  # Max width/height
JPEG_QUALITY = 85  # JPEG quality (85 is good for web)
MAX_FILE_SIZE = 500 * 1024  # 500KB max

def compress_image(input_path, output_path):
    """Compress and resize image"""
    try:
        img = Image.open(input_path)
        
        # Convert to RGB if necessary (for PNG with transparency)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize if too large
        width, height = img.size
        if width > MAX_SIZE or height > MAX_SIZE:
            if width > height:
                new_width = MAX_SIZE
                new_height = int(height * MAX_SIZE / width)
            else:
                new_height = MAX_SIZE
                new_width = int(width * MAX_SIZE / height)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Save with compression
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        img.save(output_path, 'JPEG', quality=JPEG_QUALITY, optimize=True)
        
        # Check file size, reduce quality if still too large
        file_size = os.path.getsize(output_path)
        if file_size > MAX_FILE_SIZE:
            quality = JPEG_QUALITY
            while file_size > MAX_FILE_SIZE and quality > 30:
                quality -= 10
                img.save(output_path, 'JPEG', quality=quality, optimize=True)
                file_size = os.path.getsize(output_path)
        
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        print(f"  Compressed: {os.path.basename(input_path)} ({original_size/1024:.1f}KB → {compressed_size/1024:.1f}KB)")
        return True
    except Exception as e:
        print(f"  Error compressing {input_path}: {e}")
        return False

def main():
    # Create output directory
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)
    
    # Process all case folders
    total = 0
    compressed = 0
    
    for case_name in sorted(os.listdir(CASES_DIR)):
        case_path = os.path.join(CASES_DIR, case_name)
        if not os.path.isdir(case_path):
            continue
        
        output_case_path = os.path.join(OUTPUT_DIR, case_name)
        os.makedirs(output_case_path, exist_ok=True)
        
        # Copy info.txt
        info_file = os.path.join(case_path, 'info.txt')
        if os.path.exists(info_file):
            shutil.copy2(info_file, output_case_path)
        
        # Compress images
        for fname in sorted(os.listdir(case_path)):
            if fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                input_path = os.path.join(case_path, fname)
                output_path = os.path.join(output_case_path, os.path.splitext(fname)[0] + '.jpg')
                
                print(f"[{case_name}] Processing {fname}...", end=" ", flush=True)
                if compress_image(input_path, output_path):
                    compressed += 1
                total += 1
    
    print(f"\n{'='*50}")
    print(f"DONE: {compressed}/{total} images compressed")
    print(f"Output directory: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
