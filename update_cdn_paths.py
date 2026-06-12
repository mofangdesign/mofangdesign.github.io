import re

# Read the HTML file
with open(r"D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\index.html", 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all image paths in portfolioData
# Pattern: 'cases/...'
pattern = r"'(cases/[^']+\.(jpg|jpeg|png))'"
replacement = r"CDN_BASE+'\1'"

content = re.sub(pattern, replacement, content)

# Write back
with open(r"D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\index.html", 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! All image paths updated to use CDN_BASE")
