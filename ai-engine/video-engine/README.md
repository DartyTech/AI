# Darty Video Engine

Core utilities for video generation and post-processing.

This module is designed to:
- sample frames from existing videos
- generate new frames using Darty/2GP2 models
- apply neural post-processing and edits
- render final sequences back into standard video formats

The code here is framework-agnostic:
you can plug in PyTorch, JAX or external inference endpoints
by implementing the `BaseVideoGenerator` interface in `generator.py`.
