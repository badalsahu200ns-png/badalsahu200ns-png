import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from rembg import remove


OUTPUT = Path("source-prepped.png")


def main():
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py hero.png")
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    print("Removing background with U2Net...")

    source = Image.open(input_path).convert("RGBA")
    result = remove(source)

    # Save temporary transparent image
    result_path = Path("_transparent.png")
    result.save(result_path)

    # Open using OpenCV
    img = cv2.imread(str(result_path), cv2.IMREAD_UNCHANGED)

    if img is None:
        raise RuntimeError("Unable to read processed image.")

    # Extract alpha
    alpha = img[:, :, 3]

    # Find foreground
    ys, xs = np.where(alpha > 15)

    if len(xs) == 0 or len(ys) == 0:
        raise RuntimeError("No foreground detected.")

    x1, x2 = xs.min(), xs.max()
    y1, y2 = ys.min(), ys.max()

    # Add padding
    padding = int(max(x2 - x1, y2 - y1) * 0.08)

    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(img.shape[1], x2 + padding)
    y2 = min(img.shape[0], y2 + padding)

    cropped = img[y1:y2, x1:x2]

    # Convert to grayscale
    bgr = cropped[:, :, :3]
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    # CLAHE contrast enhancement
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    # Slight sharpening
    enhanced = cv2.GaussianBlur(enhanced, (0, 0), 1)
    enhanced = cv2.addWeighted(
        gray,
        1.5,
        enhanced,
        -0.5,
        0
    )

    # Resize
    enhanced = cv2.resize(
        enhanced,
        (320, 320),
        interpolation=cv2.INTER_AREA
    )

    # Save
    cv2.imwrite(str(OUTPUT), enhanced)

    result_path.unlink(missing_ok=True)

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
