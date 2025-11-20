from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable

import cv2
import numpy as np

from .config import VideoConfig, Paths


class BaseVideoGenerator(ABC):
    """
    Абстракция над любой video-AI моделью.

    Реальная модель (например, 2GP2) должна унаследоваться от этого класса
    и реализовать метод `generate_sequence`.
    """

    @abstractmethod
    def generate_sequence(
        self,
        prompt: str,
        num_frames: int,
        cfg: VideoConfig,
    ) -> list[np.ndarray]:
        """
        Возвращает список кадров (H, W, 3) в BGR-формате (как в OpenCV).
        """
        raise NotImplementedError


class DummyGradientGenerator(BaseVideoGenerator):
    """
    Простая заглушка для примеров и тестов.
    Генерирует градиентное "видео", чтобы показать полный pipeline.
    """

    def generate_sequence(
        self,
        prompt: str,
        num_frames: int,
        cfg: VideoConfig,
    ) -> list[np.ndarray]:
        frames: list[np.ndarray] = []
        h, w = cfg.height, cfg.width

        for i in range(num_frames):
            alpha = i / max(num_frames - 1, 1)
            base = np.zeros((h, w, 3), dtype=np.uint8)
            base[:, :, 0] = int(255 * alpha)
            base[:, :, 1] = int(255 * (1 - alpha))
            base[:, :, 2] = 64

            cv2.putText(
                base,
                f"2GP2 demo frame {i+1}",
                (32, 64),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            frames.append(base)

        return frames


def generate_video_from_prompt(
    prompt: str,
    generator: BaseVideoGenerator,
    paths: Paths,
    cfg: VideoConfig,
    num_frames: int = 96,
) -> Path:
    frames = generator.generate_sequence(prompt, num_frames=num_frames, cfg=cfg)

    # сохраняем кадры на диск, чтобы потом собрать через ffmpeg
    frame_paths: list[Path] = []
    for idx, frame in enumerate(frames):
        frame_path = paths.frames_dir / f"gen_{idx:06d}.png"
        cv2.imwrite(str(frame_path), frame)
        frame_paths.append(frame_path)

    return paths.output_path
