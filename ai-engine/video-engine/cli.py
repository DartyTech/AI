import argparse

from .config import VideoConfig, Paths
from .generator import DummyGradientGenerator, generate_video_from_prompt
from .renderer import render_video_from_frames


def main():
    parser = argparse.ArgumentParser(description="Darty Video Engine CLI")
    parser.add_argument("--prompt", type=str, required=True, help="Text prompt")
    parser.add_argument("--workdir", type=str, default="video_run", help="Working directory")
    parser.add_argument("--frames", type=int, default=96, help="Number of frames")
    args = parser.parse_args()

    cfg = VideoConfig()
    paths = Paths.in_workdir(args.workdir)
    gen = DummyGradientGenerator()

    print(f"[video-engine] Generating sequence for prompt: {args.prompt!r}")
    generate_video_from_prompt(args.prompt, gen, paths, cfg, num_frames=args.frames)

    print("[video-engine] Rendering video via ffmpeg…")
    out = render_video_from_frames(paths, cfg)
    print(f"[video-engine] Done → {out}")


if __name__ == "__main__":
    main()
