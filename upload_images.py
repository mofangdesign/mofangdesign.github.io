import os, sys, base64, requests, json, time

TOKEN = "REDACTED_OLD_TOKEN"
REPO = "CHANMEIEN/mofang-design"
BRANCH = "main"
BASE_PATH = r"D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

api_base = f"https://api.github.com/repos/{REPO}/contents/"

def upload_file(rel_path):
    """Upload a single file to GitHub via the API"""
    file_path = os.path.join(BASE_PATH, rel_path)
    
    # Read file content
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # Skip if file is too large (> 50MB)
    if len(content) > 50 * 1024 * 1024:
        print(f"  SKIP (too large): {rel_path} ({len(content)} bytes)")
        return False
    
    content_b64 = base64.b64encode(content).decode('utf-8')
    
    # GitHub API path (URL encode the repo path)
    api_path = f"mofang-showcase/{rel_path}".replace("\\", "/")
    url = api_base + api_path
    
    body = {
        "message": f"Upload image",
        "content": content_b64,
        "branch": BRANCH
    }
    
    try:
        resp = requests.put(url, headers=headers, json=body, timeout=60)
        if resp.status_code == 201:
            print(f"  OK: {rel_path}")
            return True
        elif resp.status_code == 422:
            print(f"  SKIP (exists): {rel_path}")
            return True
        else:
            print(f"  FAIL: {rel_path} ({resp.status_code}): {resp.json().get('message', '')[:100]}")
            return False
    except Exception as e:
        print(f"  ERR: {rel_path} - {str(e)[:100]}")
        return False


def main():
    cases_dir = os.path.join(BASE_PATH, "cases")
    ext_set = {'.jpg', '.jpeg', '.png'}
    
    # Collect all image files
    all_images = []
    for case_name in sorted(os.listdir(cases_dir)):
        case_path = os.path.join(cases_dir, case_name)
        if not os.path.isdir(case_path):
            continue
        for fname in sorted(os.listdir(case_path)):
            if fname.startswith('.'):
                continue
            ext = os.path.splitext(fname)[1].lower()
            if ext in ext_set:
                rel = os.path.relpath(os.path.join(case_path, fname), BASE_PATH)
                all_images.append((case_name, rel))
    
    total = len(all_images)
    print(f"Found {total} images to upload\n")
    
    ok = 0
    fail = 0
    for i, (case_name, rel) in enumerate(all_images):
        name = os.path.basename(rel)
        print(f"[{i+1}/{total}] {case_name}/{name}", end="... ", flush=True)
        if upload_file(rel):
            ok += 1
        else:
            fail += 1
        # Rate limit: GitHub allows ~5000 req/hour, but slow down to be safe
        if (i + 1) % 10 == 0:
            print(f"\n--- Progress: {ok} ok, {fail} failed ---\n")
            time.sleep(1)
    
    print(f"\n{'='*50}")
    print(f"DONE: {ok} uploaded, {fail} failed out of {total}")

if __name__ == "__main__":
    main()
