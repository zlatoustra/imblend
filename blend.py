""" Simple image blending.

For details see
https://becominghuman.ai/image-blending-using-laplacian-pyramids-2f8e9982077f
"""
import cv2
import numpy as np


def pyramids(img, nlevels=3):
  """Returns Gaussian and Laplacian pyramids of the image."""
  gaussian = [np.array(img)]
  for _ in range(nlevels):
    gaussian.append(cv2.pyrDown(gaussian[-1]))

  laplacian = []
  for i in range(nlevels):
    up = cv2.pyrUp(gaussian[~i])
    laplacian.append(gaussian[~i - 1] - up)
  return gaussian, laplacian


def madd(first, second):
  """Masked addition of the images."""
  width = first.shape[1]
  return np.hstack([first[:, :width // 2], second[:, width // 2:]])


def blend(first, second, nlevels=6):
  """Blends two images."""
  first, second = pyramids(first, nlevels), pyramids(second, nlevels)
  up = madd(cv2.pyrUp(first[0][-1]), cv2.pyrUp(second[0][-1]))
  first, second = first[1], second[1]
  for i in range(nlevels):
    result = up + madd(first[i], second[i])
    up = cv2.pyrUp(result)
  return result


apple = cv2.imread("orange.jpg")
orange = cv2.imread("apple.jpg")
result = blend(orange, apple)


cv2.imshow("apple", apple)
cv2.imshow("orange", orange)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("result.jpg", result)
