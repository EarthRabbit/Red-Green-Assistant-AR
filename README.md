# Red-Green-Assistant-AR
Helping color-deficient(especially, for protanopia) with AR

## Modules used for this Assistant
* Numpy
* cv2

# Description
 People with protanopia do not perceive red as red; instead, they see it as yellow or dark. In severe cases, they may have difficulty distinguishing between colors.
 In this case, I aim to create a model that enhances visual perception by replacing red regions with a distinguishable green color ([0, 255, 0]) and outlining those areas with borders, making them easier for people to recognize.

## How?

1. Original Image
* Same

2. Protanopia Simulation
* Change BGR image to RGB, RGB to LMS image
* Change color with protanopia matrix (Brettel et al. 1997)
```bibtex
[0.0, 1.05118294, -0.05116099],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
```
* Change LMS image to RGB image, show

3. AR Enhanced
* Detect red regions in HSV color space (captures both low and high hue ranges for red)
* Replace detected red regions with a vivid green color (to enhance visibility for red-weak viewers)
* Draw black contours around the modified regions (to emphasize object boundaries clearly), show

# Results
![Image](https://github.com/user-attachments/assets/e0445cc8-1ad7-47c4-8965-892593532bb1)
![Image](https://github.com/user-attachments/assets/b6f4410e-80a4-4e53-946d-d7c6f949962a)
Image with 5, 10(changed to green and original green, distinguishable)