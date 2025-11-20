from video-engine.config import VideoConfig, Paths
from video-engine.generator import DummyGradientGenerator, generate_video_from_prompt
from video-engine.renderer import render_video_from_frames


def run():
    cfg = VideoConfig(width=720, height=404, fps=24)
    paths = Paths.in_workdir("demo_run", video_name="2gp2_demo.mp4")
    gen = DummyGradientGenerator()

    prompt = "neon cyberpunk city, camera pan, volumetric light"
    generate_video_from_prompt(prompt, gen, paths, cfg, num_frames=120)
    out = render_video_from_frames(paths, cfg)

    print(f"Demo video saved to: {out}")


if __name__ == "__main__":
    run()
