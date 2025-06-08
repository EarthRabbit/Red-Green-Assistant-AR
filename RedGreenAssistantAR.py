import cv2
import numpy as np

def simulate_protanopia(img):
    rgb_to_lms = np.array([
        [0.31399022, 0.63951294, 0.04649755],
        [0.15537241, 0.75789446, 0.08670142],
        [0.01775239, 0.10944209, 0.87256922]
    ])
    lms_to_rgb = np.linalg.inv(rgb_to_lms)

    protan_matrix = np.array([
        [0.0, 1.05118294, -0.05116099],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ])

    img = img.astype(np.float32) / 255.0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    lms = img @ rgb_to_lms.T
    sim_lms = lms @ protan_matrix.T
    sim_rgb = sim_lms @ lms_to_rgb.T
    sim_rgb = np.clip(sim_rgb, 0, 1)
    return cv2.cvtColor((sim_rgb * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)

def get_red_mask(hsv_img):
    lower_red1 = np.array([0, 35, 35])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 35, 35])
    upper_red2 = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv_img, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_img, lower_red2, upper_red2)
    return cv2.bitwise_or(mask1, mask2)

def apply_ar_filter(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = get_red_mask(hsv)

    corrected = frame.copy()
    corrected[red_mask > 0] = [0, 255, 0]

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(corrected, contours, -1, (0, 0, 0), 2)

    output = frame.copy()
    mask_3ch = cv2.merge([red_mask]*3) > 0
    output[mask_3ch] = corrected[mask_3ch]

    return output

def label_img(img, text):
    labeled = img.copy()
    cv2.putText(labeled, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    return labeled

def process_and_display_resized(input_path, display_width=1080):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Failed to open input video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        sim = simulate_protanopia(frame)
        ar = apply_ar_filter(frame)

        labeled_original = label_img(frame, "Original")
        labeled_sim = label_img(sim, "Protanopia Sim")
        labeled_ar = label_img(ar, "AR Enhanced")

        combined = np.hstack([labeled_original, labeled_sim, labeled_ar])

        h, w = combined.shape[:2]
        scale = display_width / w
        resized = cv2.resize(combined, (display_width, int(h * scale)))

        cv2.imshow("Comparison (Original | Simulation | AR)", resized)

        key = cv2.waitKey(10)
        if key == ord(' '):
            key = cv2.waitKey()
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# --- 실행 ---
if __name__ == "__main__":
    process_and_display_resized("test.mp4", display_width=1080)