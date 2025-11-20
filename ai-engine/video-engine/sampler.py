from pathlib import Path
from typing import Iterable

import cv2  # opencv-python

from .config import VideoConfig, Paths


def sample_frames(
    video_path: str | Path,
    paths: Paths,
    cfg: VideoConfig,
    every_n_frames: int = 1,
) -> list[Path]:
    """
    Extract frames from an existing video.

    Returns a list of saved frame paths.
    """
    video_path = Path(video_path)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")

    frame_paths: list[Path] = []
    idx = 0
    saved = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx % every_n_frames == 0:
            frame = cv2.resize(frame, (cfg.width, cfg.height))
            frame_path = paths.frames_dir / f"frame_{saved:06d}.png"
            cv2.imwrite(str(frame_path), frame)
            frame_paths.append(frame_path)
            saved += 1

        idx += 1

    cap.release()
    return frame_paths


def iter_frames(frame_paths: Iterable[Path]):
    """Lazy загрузка кадров (например, для генератора/редактора)."""
    for p in frame_paths:
        img = cv2.imread(str(p))
        if img is None:
            continue
        yield p, img
