from PIL import Image
import numpy as np

img = Image.open(r'D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\logo.jpg').convert('RGBA')
arr = np.array(img, dtype=np.uint8)
print('Input shape:', arr.shape)

h, w, _ = arr.shape
result = np.zeros((h, w, 4), dtype=np.uint8)

for i in range(h):
    for j in range(w):
        r, g, b, a = int(arr[i,j,0]), int(arr[i,j,1]), int(arr[i,j,2]), int(arr[i,j,3])
        brightness = (r + g + b) / 3
        if brightness > 230:
            result[i,j] = [0, 0, 0, 0]
        else:
            alpha = int(255 - brightness * 1.2)
            alpha = max(0, min(255, alpha))
            result[i,j] = [255, 255, 255, alpha]

out = Image.fromarray(result, 'RGBA')
# Resize
max_dim = 500
ratio = min(max_dim / w, max_dim / h, 1.0)
if ratio < 1.0:
    new_w, new_h = int(w * ratio), int(h * ratio)
    out = out.resize((new_w, new_h), Image.LANCZOS)
    print('Resized to:', new_w, 'x', new_h)

out.save(r'D:\WODK BUDDY\2026-06-11-20-06-00\mofang-showcase\logo.png')
print('Done! Saved logo.png size:', out.size)
