# Image Generation Tool

## Description
Generates images from text descriptions using Stable Diffusion XL running locally via the `diffusers` library. Produces high-quality 1024x1024 images in approximately 15 seconds on an M2 MacBook Pro.

## Parameters
- `prompt` (required): Text description of the desired image. Be specific about style, lighting, and composition.
- `negative_prompt` (optional): What to exclude from the image. Default: "blurry, low quality, distorted".
- `width` (optional): Image width in pixels. Must be multiple of 8. Default: 1024.
- `height` (optional): Image height in pixels. Must be multiple of 8. Default: 1024.
- `num_steps` (optional): Diffusion steps. More steps = better quality but slower. Default: 30.
- `seed` (optional): Random seed for reproducibility. Default: random.

## Example Usage
```python
image = generate_image(
    prompt="A serene Japanese garden at sunset, watercolor painting style, soft lighting",
    negative_prompt="photorealistic, harsh shadows",
    num_steps=40,
    seed=42
)
# Returns: {"path": "/tmp/generated_abc123.png", "seed": 42, "generation_time_s": 14.2}
```

## Supported Styles
The model responds well to style keywords: "oil painting", "watercolor", "digital art", "photograph", "pencil sketch", "anime style", "pixel art", "3D render".

## Output
- Images saved to `/tmp/generated_<uuid>.png`
- Metadata saved alongside as `.json` file
- Images are automatically cleaned up after 24 hours

## Limitations
- Maximum resolution: 2048x2048
- NSFW content filter is enabled and cannot be disabled
- Batch generation not supported (one image at a time)
