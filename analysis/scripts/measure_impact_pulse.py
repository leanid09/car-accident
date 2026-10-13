# Measures frame-to-frame global image motion of the side-camera export around the
# impact. The camera is rigidly mounted to the body, so once the vehicle is
# stationary, any image-wide shift is body motion — and a stationary car's body
# moves vertically only on its suspension.
#
# Usage:
#   ffmpeg -ss 21.5 -to 26.0 -i "videos/2026-08-07-04-46-26 3.MP4" frames/f_%03d.png
#   python3 measure_impact_pulse.py frames/
#
# Method: FFT phase correlation with sub-pixel parabolic refinement, on a static
# background strip (building + sky, rows 15-115 of the 724x510 frame). The strip's
# left and right halves are measured independently: a shift that appears in both,
# in the same direction at the same instant, is global camera (body) motion, not
# an object moving through one part of the scene.

import sys, glob
import numpy as np
from PIL import Image

def load(path, x0, x1):
    im = np.asarray(Image.open(path).convert("L"), dtype=np.float64)
    return im[15:115, x0:x1]

def phase_shift(a, b):
    win = np.outer(np.hanning(a.shape[0]), np.hanning(a.shape[1]))
    A, B = np.fft.rfft2(a * win), np.fft.rfft2(b * win)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-9
    c = np.fft.irfft2(R, a.shape)
    peak = np.unravel_index(np.argmax(c), c.shape)
    dy, dx = peak
    if dy > a.shape[0] // 2: dy -= a.shape[0]
    if dx > a.shape[1] // 2: dx -= a.shape[1]
    def refine(cm, p, n):
        m1, m0, m2 = cm[(p - 1) % n], cm[p], cm[(p + 1) % n]
        return (m1 - m2) / (2 * (m1 - 2 * m0 + m2) + 1e-12)
    return dy + refine(c[:, peak[1]], peak[0], c.shape[0]), \
           dx + refine(c[peak[0], :], peak[1], c.shape[1])

def main(frame_dir, t0=21.5, fps=24.0):
    files = sorted(glob.glob(f"{frame_dir}/f_*.png"))
    print("t(s)    full-strip dy,dx    left-half dy,dx    right-half dy,dx")
    for i in range(1, len(files)):
        t = t0 + i / fps
        dyf, dxf = phase_shift(load(files[i], 10, 714), load(files[i - 1], 10, 714))
        dyl, dxl = phase_shift(load(files[i], 10, 360), load(files[i - 1], 10, 360))
        dyr, dxr = phase_shift(load(files[i], 364, 714), load(files[i - 1], 364, 714))
        print(f"{t:6.3f}  {dyf:6.2f},{dxf:6.2f}    {dyl:6.2f},{dxl:6.2f}    {dyr:6.2f},{dxr:6.2f}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "frames")
