

from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage.filters import gaussian_filter
from matplotlib import pyplot as plt


__author__ = 'Junya Kaneko<jyuneko@hotmail.com>'


class MoravecCornerDetector:
    def __init__(self, threshold=0.03, error_window=(3, 3), selection_window=(3, 3)):
        self._threshold = threshold
        self._error_window = error_window
        self._selection_window = selection_window

    def _evaluate_error(self, image, start, shift):
        e = 0
        for row in range(self._error_window[0]):
            for col in range(self._error_window[1]):
                image_row = start[0] + row
                image_col = start[1] + col
                e += np.power(image[image_row + shift[0], image_col + shift[1]] - image[image_row, image_col], 2)
        return e

    def _get_minimum(self, image, start):
        shifts = ((0, 1), (1, 1), (1, 0), (-1, 1))
        #shifts = ((-1, -1), (-1, 0), (0, -1), (1, 1), (1, 0), (0, 1), (-1, 1), (1, -1))
        min = np.infty
        for shift in shifts:
            e = self._evaluate_error(image, start, shift)
            min = e if e < min else min
        return min

    def _get_minima(self, image):
        minima = np.zeros(image.shape)
        for row in range(1, image.shape[0] - self._error_window[0] - 1):
            for col in range(1, image.shape[1] - self._error_window[1] - 1):
                minima[row, col] = self._get_minimum(image, (row, col))
        return minima

    def detect(self, image, threshold=None):
        threshold = threshold if threshold is not None else self._threshold
        minima = self._get_minima(image)
        corners = [[], []]
        for row in range(minima.shape[0] - self._selection_window[0]):
            for col in range(minima.shape[1] - self._selection_window[1]):
                arg = np.argmax(minima[row:row + self._selection_window[0], col:col + self._selection_window[1]])
                _row = row + int(arg/self._selection_window[1])
                _col = col + arg % self._selection_window[1]
                if minima[_row, _col] > threshold:
                    corners[0].append(_row)
                    corners[1].append(_col)
        return np.array(corners)

if __name__ == '__main__':
    def get_rectangle(start, size):
        rectangle = Image.new('L', (280, 280), color=255)
        draw = ImageDraw.Draw(rectangle)
        draw.rectangle((start, size))
        del draw
        return gaussian_filter(np.array(rectangle, dtype=np.float)/255, 1.0)

    def get_ellipse(start, size):
        ellipse = Image.new('L', (280, 280), color=255)
        draw = ImageDraw.Draw(ellipse)
        draw.ellipse((start, size))
        del draw
        return gaussian_filter(np.asarray(ellipse, dtype=np.float)/255, 1.0)

    def get_partial_triangle(start, middle, theta):
        start = start if isinstance(start, np.ndarray) else np.array(start)
        middle = middle if isinstance(middle, np.ndarray) else np.array(middle)
        norm = np.linalg.norm(middle - start)
        partial_triangle = Image.new('L', (280, 280), color=255)
        draw = ImageDraw.Draw(partial_triangle)
        draw.line((tuple(start), tuple(middle), tuple(middle + np.array([norm * np.cos(theta), norm * np.sin(theta)]))))
        del draw
        return gaussian_filter(np.array(partial_triangle, dtype=np.float)/255, 3.0)


    rectangle = get_rectangle((20, 20), (50, 70))
    ellipse = get_ellipse((50, 50), (100, 150))

    images = [rectangle, ellipse, ] + [get_partial_triangle((50, 50), (100, 50), theta/180 * np.pi) for theta in range(0, 360, 15)]

    for i, image in enumerate(images):
        moravec = MoravecCornerDetector(0.0)
        corners = moravec.detect(image)

        plt.figure(i)
        plt.imshow(image, cmap="Greys_r")
        plt.scatter(corners[1], corners[0], color='red')
        plt.savefig('images/%s.png' % i)
        plt.close()
