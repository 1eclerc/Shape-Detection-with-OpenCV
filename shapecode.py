# cse307 - görüntü işleme
# uygulama sınavı
# lecturer: Dr. Mahmut Sinecen
# student: Ali Cemal Gülmez - 211805078


# opencv kütüphanesi 
import cv2
import numpy as np

def detect_shapes(image_path):
    # görüntüyü okuma
    image = cv2.imread(image_path)
    if image is None:
        print(f"Hata: {image_path} görüntüsü okunamadı.")
        return
    
    # sonuçları göstermek için kopyasını oluşturma
    output = image.copy()
    
    # grayscaling
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # gaussian blur - gürültüyü azaltma
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Hough Circle Transform için özel bir kopya
    circle_detection = blurred.copy()
    
    # kenar tespiti için canny
    edges = cv2.Canny(blurred, 50, 150)
    
    # kenarları daha kalın görme
    dilated = cv2.dilate(edges, None, iterations=1)
    
    # contours
    contours, _ = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Hough Circle Transform
    circles = cv2.HoughCircles(
        circle_detection, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=20, 
        param1=50, 
        param2=30, 
        minRadius=10, 
        maxRadius=300
    )
    
    # tespit edilen daireleri saklamak için set
    detected_circles = set()
    
    # Hough ile tespit edilen daireler varsa
    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # daire merkezi ve yarıçapı
            center_x, center_y = circle[0], circle[1]
            radius = circle[2]
            
            # merkez koordinatlarını sete ekle (daha sonraki karşılaştırmalar için)
            detected_circles.add((center_x, center_y))
            
            # daireyi çiz
            cv2.circle(output, (center_x, center_y), radius, (255, 0, 0), 2)
            # merkezi işaretle
            cv2.circle(output, (center_x, center_y), 2, (0, 0, 255), 3)
            # daire yazısı
            cv2.putText(output, "Daire", (center_x - 20, center_y), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # her kontur için
    for contour in contours:
        # çok küçük konturları geçme eşiği
        if cv2.contourArea(contour) < 100:
            continue
        
        # kontur yaklaşıklığını hesaplama
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # konturun merkezini bulma
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
        
        # daire olarak işaretlendi mi kontrol et
        is_marked_circle = False
        for (circle_x, circle_y) in detected_circles:
            # merkez kontrolü
            if abs(circle_x - cX) < 20 and abs(circle_y - cY) < 20:
                is_marked_circle = True
                break
        
        # daire olarak işaretlendiyse, bu konturu atla
        if is_marked_circle:
            continue
            
        # kontur rengini çizme - yeşille
        cv2.drawContours(output, [approx], -1, (0, 255, 0), 2)
        
        # şekli kenar sayısına göre tanımlama
        shape_name = ""
        vertices = len(approx)
        
        if vertices == 3:
            shape_name = "Ucgen"
        elif vertices == 4:
            # hangisi kare hangisi dikdörtgen ayırma
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05:
                shape_name = "Kare"
            else:
                shape_name = "Dikdortgen"
        elif vertices == 5:
            shape_name = "Besgen"
        elif vertices > 5:
            # daire tespit edilemeyenler için yedek yöntem
            perimeter = cv2.arcLength(contour, True)
            area = cv2.contourArea(contour)
            circularity = 4 * np.pi * area / (perimeter * perimeter)
            
            if circularity > 0.8:  # daha yüksek eşik değeri
                shape_name = "Daire"
            else:
                shape_name = "Cokgen"
        
        # şekil adını merkeze yazma
        cv2.putText(output, shape_name, (cX - 20, cY), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
    
    # kenar tespitini gösterme
    cv2.imshow("Kenarlar", dilated)
    
    # sonuçlar
    cv2.imshow("Sekil Tespiti", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # görüntü yolu
    image_path = "shapes.jpg"
    detect_shapes(image_path)