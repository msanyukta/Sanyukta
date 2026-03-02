# CLAUDE.md — Ad Creative Generator

## Project Overview

This project generates Facebook and Instagram ad creative for e-commerce brands
using Nano Banana 2 with structured JSON prompting. It is designed to streamline
the creation, iteration, and organization of paid social ad assets.

No build system or test suite exists — this is a creative asset store. The
primary workflow is: **brief → JSON prompt → generated image → feedback → iterate.**

---

## Technology Stack

- **Image generation**: Nano Banana 2 via the fal.ai API (`fal-ai/nano-banana-2`)
- **Generation script**: `scripts/generate.py` (Python, requires `FAL_KEY` env var)
- **Prompt skill**: `.claude/skills/nanobanana.md` — always use this skill to build prompts
- **Prompt format**: Structured JSON (never plain text)
- **Platform targets**: Facebook Feed, Instagram Feed, Stories, Reels, Carousel

---

## Directory Structure

```
/
├── CLAUDE.md                          # This file
├── .claude/
│   └── skills/
│       └── nanobanana.md              # Nano Banana 2 prompt-building skill
├── scripts/
│   └── generate.py                    # Image generation script
├── prompts/                           # JSON prompt files, organized by ad category
│   ├── product-hero/                  # studio-product-hero style
│   ├── lifestyle/                     # lifestyle-in-context style
│   ├── ugc-style/                     # ugc-selfie style
│   ├── before-after/                  # before-after style
│   ├── infographics/                  # flat-lay, editorial-beauty styles
│   └── social-proof/                  # unboxing-moment and social proof styles
└── images/                            # Generated image outputs, mirroring prompts/
    ├── product-hero/
    ├── lifestyle/
    ├── ugc-style/
    ├── before-after/
    ├── infographics/
    └── social-proof/
```

---

## Running the Generation Script

```bash
FAL_KEY=<your-key> python scripts/generate.py prompts/<category>/<filename>.json
```

The script:
1. Reads the JSON prompt file
2. Posts to `https://fal.run/fal-ai/nano-banana-2` with the `FAL_KEY` auth header
3. Downloads the returned image and saves it locally

> **Important**: The script currently saves output with a timestamp filename
> (`images/<timestamp>.png`). After running, **manually rename and move** the
> file to `images/<category>/{product}-{style}-{variation}.png` to match the
> naming convention.

---

## File Naming Convention

```
{product}-{style}-{variation}.json   # prompt files
{product}-{style}-{variation}.png    # image files
```

**Examples:**
- `vitamin-c-serum-ugc-selfie-01.json`
- `protein-powder-lifestyle-kitchen-02.json`
- `face-mask-before-after-split-01.json`

Rules:
- Always lowercase
- Hyphen-separated tokens
- No spaces or underscores
- Never overwrite — increment the variation number (`-01`, `-02`, `-03`, …)

---

## Rules — Follow These at All Times

1. Use the **`nanobanana` skill** for ALL image generation — never use another tool or method.
2. All prompts must use **structured JSON** — never plain-text prompts.
3. Every prompt must include a **`negative_prompt`** field.
4. Always save prompts as `.json` files in the matching `prompts/<category>/` subfolder.
5. Always save images in the matching `images/<category>/` subfolder.
6. Never overwrite an existing file — increment the variation number.
7. When unsure about a brand's visual style, **ask before generating** rather than guessing.

---

## Default Aspect Ratios

| Placement              | Aspect Ratio | Resolution  |
|------------------------|-------------|-------------|
| Facebook / Instagram Feed | `4:5`    | `1536x1536` |
| Stories / Reels        | `9:16`      | `1536x1536` |
| Carousel ads           | `1:1`       | `1536x1536` |
| Landing page hero      | `16:9`      | `2048x2048` |

If the user doesn't specify a platform, default to **Facebook Feed (4:5)**.

---

## JSON Prompt Schema

```json
{
  "prompt": "Detailed visual description of the ad creative",
  "negative_prompt": "Elements to exclude",
  "settings": {
    "resolution": "1024x1024 | 1536x1536 | 2048x2048",
    "aspect_ratio": "1:1 | 4:5 | 16:9 | 9:16",
    "style": "ugc-selfie | lifestyle-in-context | studio-product-hero | flat-lay | before-after | editorial-beauty | unboxing-moment",
    "lighting": "ring-light | natural-window | golden-hour | studio-softbox | bathroom-vanity | dramatic-rim | overhead-natural",
    "camera": {
      "lens": "24mm | 35mm | 50mm | 85mm | 105mm | 200mm",
      "angle": "eye-level | low-angle | high-angle | overhead | dutch-angle",
      "framing": "extreme-close-up | close-up | medium | full-body | wide",
      "height": "ground-level | waist-level | eye-level | elevated",
      "depth_of_field": "shallow | moderate | deep",
      "focus": "subject | background | split"
    },
    "color_grading": "warm | cool | neutral | muted | vibrant | cinematic"
  }
}
```

Default `negative_prompt`:
```
"blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel"
```

---

## Ad Creative Styles

| Style | Description |
|---|---|
| `ugc-selfie` | Shot on iPhone look. Ring light or natural window. Casual, authentic, not polished. |
| `lifestyle-in-context` | Product in a real environment — kitchen counter, bathroom shelf, gym bag, desk. |
| `studio-product-hero` | Clean white or gradient background. Perfect even lighting. Catalog ads and hero images. |
| `flat-lay` | Overhead shot. Product surrounded by complementary items. Great for carousel ads. |
| `before-after` | Split composition or side-by-side. Clear transformation. Same lighting on both sides. |
| `editorial-beauty` | High-end magazine look. Dramatic lighting. Bold composition. Premium positioning. |
| `unboxing-moment` | Hands opening a package or holding a product. Excitement and discovery. |

---

## Style-Specific Defaults

Apply these before user overrides when building prompts:

**`ugc-selfie`**
- lighting: `ring-light`
- camera: `35mm`, `eye-level`, `medium` framing, `shallow` DoF
- color_grading: `warm`
- prompt **must** include: `"shot on iPhone, slight motion blur, casual composition, imperfect framing"`
- for people, **must** include: `"visible pores, natural skin texture, subtle blemishes"`

**`lifestyle-in-context`**
- lighting: `natural-window`
- camera: `35mm` or `50mm`, `eye-level`, `medium` or `wide`, `moderate` DoF
- color_grading: `warm` or `neutral`

**`studio-product-hero`**
- lighting: `studio-softbox`
- camera: `85mm` or `105mm`, `eye-level` or `high-angle`, `close-up`, `shallow` DoF
- color_grading: `neutral` or `cool`

**`flat-lay`**
- lighting: `overhead-natural`
- camera: any lens, `overhead`, `wide`, `deep` DoF
- color_grading: `warm` or `vibrant`

**`before-after`**
- lighting: `studio-softbox` (consistent across both halves)
- camera: `50mm` or `85mm`, `eye-level`, `medium`, `moderate` DoF
- color_grading: `neutral`

**`editorial-beauty`**
- lighting: `dramatic-rim`
- camera: `85mm`, `eye-level` or `low-angle`, `close-up`, `shallow` DoF
- color_grading: `cinematic`

**`unboxing-moment`**
- lighting: `natural-window` or `ring-light`
- camera: `35mm`, `eye-level` or `high-angle`, `medium`, `moderate` DoF
- color_grading: `warm`

---

## Camera Lens Quick Reference

| Lens | Best For | Ad Use Case |
|------|----------|-------------|
| `24mm` | Wide environment | Lifestyle scene with full room context |
| `35mm` | Environmental portrait | UGC selfie, person + product in context |
| `50mm` | General purpose | Versatile, natural feel |
| `85mm` | Portrait | Beauty and skincare close-ups |
| `105mm` | Product detail | Texture, ingredients, label close-up |
| `200mm` | Product isolation | Product floating against blurred background |

---

## Image Generation Workflow

Follow these steps in order for every generation request:

1. **Receive** the creative brief (plain English description from the user).
2. **Parse** the brief — extract product, style, platform, scene, model, mood, lighting, copy.
   - If any element is ambiguous, **ask the user** before proceeding.
3. **Build** a structured JSON prompt using the `nanobanana` skill.
4. **Validate** before saving:
   - `aspect_ratio` matches the target platform
   - `style` is one of the seven valid values
   - `negative_prompt` is present
   - UGC prompts include the required "shot on iPhone…" language
   - People prompts include the required "visible pores…" language
   - Product label text is spelled out exactly
   - Filename follows `{product}-{style}-{variation}.json`
   - File does not already exist (increment if needed)
5. **Save** the JSON to `prompts/<category>/<filename>.json`.
6. **Run** the generation script: `python scripts/generate.py prompts/<category>/<filename>.json`
7. **Rename and move** the output image to `images/<category>/<filename>.png`.
8. **Show** the result to the user and ask for feedback.

---

## Feedback Loop

When the user gives feedback on a generated image:

1. Identify which JSON fields need adjustment (e.g., "too dark" → `settings.lighting` or `settings.color_grading`).
2. Note explicitly what worked and what didn't.
3. Apply those preferences to **all future generations** in the session.
4. Save corrected prompts as new variations — **never overwrite** existing files.
5. If the user says "always do this", record the preference as a session default.
6. When asked, update the `nanobanana` skill defaults to encode new preferences permanently.

---

## Brand Consistency (Multi-Image Campaigns)

When generating multiple images for the same brand or campaign:

1. Lock `settings.lighting`, `settings.camera`, and `settings.color_grading` from the first approved image.
2. Copy those locked values into every subsequent prompt.
3. **Only vary** `prompt` (scene/subject description) and product-specific details.
4. Document the shared visual settings in the first prompt file so they can be copied forward.
5. If the user changes a locked field, treat it as a new visual direction and confirm before applying it to the rest of the set.

---

## Product-Specific Prompt Rules

- For **product shots**: specify exact material properties, e.g. `"matte packaging, glossy label, liquid inside glass bottle"`.
- For **text on labels**: spell out EXACTLY what it should say, e.g. `"white label reading 'Vitamin C Brightening Serum'"`.
- For **people**: always include `"visible pores, natural skin texture, subtle blemishes"` — never airbrushed plastic skin.
- For **UGC-style**: always include `"shot on iPhone, slight motion blur, casual composition, imperfect framing"`.

---

## Existing Prompt Examples

Three UGC-style prompts exist at `prompts/ugc-style/` for a vitamin C serum campaign, demonstrating consistent brand settings (all `4:5`, `warm` color grading, `ugc-selfie` style) with varied angles:

| File | Angle / Scene |
|---|---|
| `vitamin-c-serum-ugc-closeup-apply-01.json` | Extreme close-up, low-angle, applying serum to cheekbone |
| `vitamin-c-serum-ugc-mirror-selfie-01.json` | Eye-level, medium, bathroom mirror selfie |
| `vitamin-c-serum-ugc-overhead-routine-01.json` | High-angle from above, morning skincare routine GRWM |

These serve as reference implementations for brand consistency across a UGC campaign set.

---

## Environment Setup

| Variable | Purpose |
|---|---|
| `FAL_KEY` | API key for fal.ai (Nano Banana 2). Required by `scripts/generate.py`. |

---

## Development Notes for AI Assistants

- No build system or test suite — do not introduce one.
- Do not introduce any image generation method other than the `nanobanana` skill.
- All prompts must use structured JSON — never plain-text prompts.
- Every prompt must include a `negative_prompt` field.
- The `scripts/generate.py` script saves output with a timestamp filename; always rename/move the result to follow the naming convention before considering the task complete.
- When unsure about a brand's visual style, ask before generating rather than guessing.
