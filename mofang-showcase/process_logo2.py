from PIL import Image
import numpy as np

img = Image.open(r'D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\logo-mf.jpg').convert('RGBA')
arr = np.array(img, dtype=np.uint8)
print('Input shape:', arr.shape)

h, w, _ = arr.shape
result = np.zeros((h, w, 4), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        r, g, b = int(arr[i,j,0]), int(arr[i,j,1]), int(arr[i,j,2])
        brightness = (r + g + b) / 3
        if brightness < 60:
            # Dark (black bg) -> transparent
            result[i,j] = [0, 0, 0, 0]
        else:
            # White logo -> keep white, alpha based on brightness
            alpha = int(brightness * 1.2)
            alpha = max(0, min(255, alpha))
            result[i,j] = [255, 255, 255, alpha]

out = Image.fromarray(result, 'RGBA')
max_dim = 500
ratio = min(max_dim / w, max_dim / h, 1.0)
if ratio < 1.0:
    new_w, new_h = int(w * ratio), int(h * ratio)
    out = out.resize((new_w, new_h), Image.LANCZOS)
    print('Resized to:', new_w, 'x', new_h)

out.save(r'D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\logo-mf.png')
print('Done! Size:', out.size)
