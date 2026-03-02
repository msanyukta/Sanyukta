# CLAUDE.md — Ad Creative Generator

## Project Overview

This project generates Facebook and Instagram ad creative for e-commerce brands
using Nano Banana 2 with structured JSON prompting. It is designed to streamline
the creation, iteration, and organization of paid social ad assets.

---

## Technology Stack

- **Image generation**: Nano Banana 2 (via the `nanobanana` skill)
- **Prompt format**: Structured JSON
- **Platform targets**: Facebook Feed, Instagram Feed, Stories, Reels, Carousel

---

## Directory Structure

```
/
├── CLAUDE.md                        # This file
├── .claude/skills/nanobanana.md     # Nano Banana 2 prompt-building skill
├── prompts/                         # JSON prompt files, organized by ad category
│   ├── product-hero/                # studio-product-hero style
│   ├── lifestyle/                   # lifestyle-in-context style
│   ├── ugc-style/                   # ugc-selfie style
│   ├── before-after/                # before-after style
│   ├── infographics/                # flat-lay, editorial-beauty styles
│   └── social-proof/                # unboxing-moment and social proof styles
└── images/                          # Generated image outputs, mirroring prompts/
    ├── product-hero/
    ├── lifestyle/
    ├── ugc-style/
    ├── before-after/
    ├── infographics/
    └── social-proof/
```

---

## File Naming Convention

Files must be named descriptively using the pattern:

```
{product}-{style}-{variation}.json   # for prompt files
{product}-{style}-{variation}.png    # for image files
```

**Examples:**
- `vitamin-c-serum-ugc-selfie-01.json`
- `protein-powder-lifestyle-kitchen-02.json`
- `face-mask-before-after-split-01.json`

Always use lowercase, hyphen-separated tokens. No spaces or underscores.

---

## Rules — Follow These at All Times

1. Use the **`nanobanana` skill** for ALL image generation — never use another tool.
2. Always save prompts as `.json` files in the matching `prompts/<category>/` subfolder.
3. Always save images in the matching `images/<category>/` subfolder.
4. Default aspect ratios:
   - **Facebook / Instagram Feed**: `4:5`
   - **Stories / Reels**: `9:16`
   - **Carousel**: `1:1`
   - **Landing page hero**: `16:9`
5. Never overwrite an existing file — increment the variation number (e.g., `-01`, `-02`).

---

## Ad Creative Styles

| Style | Description |
|---|---|
| `ugc-selfie` | Shot on iPhone look. Ring light or natural window. Casual, authentic, not polished. |
| `lifestyle-in-context` | Product in a real environment — kitchen counter, bathroom shelf, gym bag, desk. |
| `studio-product-hero` | Clean white or gradient background. Perfect even lighting. For catalog ads and hero images. |
| `flat-lay` | Overhead shot. Product surrounded by complementary items. Great for carousel ads. |
| `before-after` | Split composition or side-by-side. Clear transformation. Same lighting on both sides. |
| `editorial-beauty` | High-end magazine look. Dramatic lighting. Bold composition. Premium positioning. |
| `unboxing-moment` | Hands opening a package or holding a product. Excitement and discovery. |

---

## Image Generation Workflow

Follow these steps in order for every generation request:

1. **Receive** the creative brief (plain English description from the user).
2. **Write** a structured JSON prompt using the `nanobanana` skill.
3. **Run** the generation script.
4. **Save** the prompt file to `prompts/<category>/` and the image to `images/<category>/`.
5. **Show** the result to the user and ask for feedback.

---

## Feedback Loop

When the user gives feedback on a generated image:

- Note explicitly what worked and what didn't.
- Apply those preferences to **all future generations** in the session.
- When asked, update the `nanobanana` skill defaults to encode new preferences permanently.

---

## Brand Consistency (Multi-Image Campaigns)

When generating multiple images for the same brand or campaign:

- **Reuse** the same lighting, color grading, and camera settings across all assets.
- **Only change** the product, model, or copy between variations.
- **Document** the shared visual settings in the first prompt file so they can be copied forward.
- The goal is a consistent visual identity across every ad in the set.

---

## Development Notes for AI Assistants

- This repository has no build system or test suite — it is a creative asset store.
- The primary workflow is: brief → JSON prompt → generated image → feedback → iterate.
- Do not introduce any image generation method other than the `nanobanana` skill.
- All prompts must use structured JSON — never plain-text prompts.
- Every prompt must include a `negative_prompt` field.
- For UGC-style images, always include "shot on iPhone, slight motion blur, casual composition, imperfect framing" in the prompt.
- For images with people, always include "visible pores, natural skin texture, subtle blemishes" for realism.
- When unsure about a brand's visual style, ask before generating rather than guessing.
