from pathlib import Path
import subprocess

from .config import VideoConfig, Paths


def render_video_from_frames(
    paths: Paths,
    cfg: VideoConfig,
    pattern: str = "gen_%06d.png",
) -> Path:
    """
    Собирает кадры вида gen_000000.png в финальное видео через ffmpeg.
    """
    input_pattern = str(paths.frames_dir / pattern)

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate",
        str(cfg.fps),
        "-i",
        input_pattern,
        *cfg.as_ffmpeg_args(),
        str(paths.output_path),
    ]

    subprocess.run(cmd, check=True)
    return paths.output_path
