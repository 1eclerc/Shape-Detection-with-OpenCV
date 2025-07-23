# 🔷 Shape Detection using OpenCV

This is a simple computer vision project that detects basic geometric shapes (circle, triangle, square, rectangle, polygon) in an image using **OpenCV**. The project uses contour detection and Hough Circle Transform to identify and label shapes visually.

---

## 📌 Features

- Detects and labels:
  - Circles (via Hough Transform and backup circularity check)
  - Triangles
  - Squares vs Rectangles (by aspect ratio)
  - Pentagons
  - Other polygons
- Uses Gaussian blur, Canny edge detection, contour approximation
- Visualizes edges and labeled results with bounding text
- Uses OpenCV drawing functions for visualization

---

## 📂 Project Structure

```
├── shapecode.py        # Main shape detection script
├── shapes.jpg          # Sample input image (replace with your own)
└── README.md           # This file
```

---

## ⚙️ Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy

Install dependencies:
```bash
pip install opencv-python numpy
```

---

## 🚀 How to Run

1. Make sure `shapecode.py` and your image file (e.g., `shapes.jpg`) are in the same directory.
2. Run the script:
```bash
python shapecode.py
```

3. Two windows will open:
   - `Kenarlar` — shows the detected edges
   - `Sekil Tespiti` — shows the labeled shapes on the image

Press any key to close the windows.

---

## 📸 Notes

- Circles are detected using both **HoughCircles** and **circularity-based fallback**.
- Shapes with fewer than 100 px area are ignored.
- You can change the input file name in the script:
```python
image_path = "shapes.jpg"
```

---

## 🪪 License

This project is for educational use.
