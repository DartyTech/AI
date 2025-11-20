from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoConfig:
    width: int = 768
    height: int = 432
    fps: int = 24
    codec: str = "libx264"
    pixel_format: str = "yuv420p"
    bitrate: str = "6M"

    def as_ffmpeg_args(self) -> list[str]:
        return [
            "-vf", f"scale={self.width}:{self.height}",
            "-r", str(self.fps),
            "-c:v", self.codec,
            "-pix_fmt", self.pixel_format,
            "-b:v", self.bitrate,
        ]


@dataclass
class Paths:
    workdir: Path
    frames_dir: Path
    output_path: Path

    @classmethod
    def in_workdir(cls, workdir: str | Path, video_name: str = "output.mp4") -> "Paths":
        workdir = Path(workdir)
        frames_dir = workdir / "frames"
        frames_dir.mkdir(parents=True, exist_ok=True)
        return cls(
            workdir=workdir,
            frames_dir=frames_dir,
            output_path=workdir / video_name,
        )
