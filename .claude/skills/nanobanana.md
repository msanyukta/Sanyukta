# Nano Banana 2 Ad Creative Skill

## Purpose

Convert plain-text ad creative briefs into structured JSON prompts for
Nano Banana 2 that produce consistent, ad-ready, realistic images for
Facebook, Instagram, and e-commerce use.

---

## When to Use This Skill

Use this skill whenever the user:
- Describes an ad they want ("Show me a hero shot of…")
- Provides a creative brief for a product or campaign
- Asks for variations on an existing ad creative
- Requests a batch of assets for a campaign

---

## JSON Prompt Schema

Always structure prompts as JSON with these fields:

```json
{
  "prompt": "Detailed visual description of the ad creative",
  "negative_prompt": "Elements to exclude",
  "settings": {
    "resolution": "1024x1024 | 1536x1536 | 2048x2048",
    "aspect_ratio": "1:1 | 4:5 | 16:9 | 9:16",
    "style": "See style guide below",
    "lighting": "See lighting guide below",
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

---

## Style Guide (Ad Creative Specific)

| Style | Description |
|---|---|
| `ugc-selfie` | Shot on iPhone look. Ring light or natural window. Slightly imperfect framing. The person is holding or using the product. Casual, authentic, not polished. |
| `lifestyle-in-context` | Product in a real environment — kitchen counter, bathroom shelf, gym bag, desk. Natural lighting. Aspirational but believable. |
| `studio-product-hero` | Clean white or gradient background. Perfect even lighting. Product centered. No distractions. For catalog ads and hero images. |
| `flat-lay` | Overhead shot. Product surrounded by complementary items (ingredients, accessories). Styled but natural. Great for carousel ads. |
| `before-after` | Split composition or side-by-side. Clear transformation. Same lighting on both sides. Commonly used for skincare, supplements, cleaning products. |
| `editorial-beauty` | High-end magazine look. Dramatic lighting. Bold composition. For premium/luxury positioning. |
| `unboxing-moment` | Hands opening a package or holding a product for the first time. Excitement and discovery. Great for DTC subscription brands. |

---

## Lighting Guide

| Lighting | Description |
|---|---|
| `ring-light` | Even, flattering facial lighting. The UGC standard. Slight catchlight in eyes. |
| `natural-window` | Soft diffused daylight. Lifestyle and product shots. |
| `golden-hour` | Warm directional sunlight. Outdoor lifestyle. |
| `studio-softbox` | Controlled, even lighting. Product hero shots. |
| `bathroom-vanity` | Warm overhead + mirror reflection. Skincare and beauty. |
| `dramatic-rim` | Hard backlight edge. Premium and editorial. |
| `overhead-natural` | Soft top-down light. Flat lay and food. |

---

## Camera Lens Quick Reference

| Lens | Best For | Ad Use Case |
|------|----------|-------------|
| 24mm | Wide environment | Lifestyle scene with full room context |
| 35mm | Environmental portrait | UGC selfie, person + product in context |
| 50mm | General purpose | Versatile, natural feel |
| 85mm | Portrait | Beauty and skincare close-ups |
| 105mm | Product detail | Texture, ingredients, label close-up |
| 200mm | Product isolation | Product floating against blurred background |

---

## Platform-Specific Defaults

| Placement | Aspect Ratio | Resolution |
|---|---|---|
| Facebook / Instagram Feed | 4:5 | 1536x1536 |
| Stories / Reels | 9:16 | 1536x1536 |
| Carousel ads | 1:1 | 1536x1536 |
| Landing page hero | 16:9 | 2048x2048 |

If the user doesn't specify a platform, default to **Facebook Feed (4:5)**.

---

## Rules

1. **ALWAYS** use JSON — never plain-text prompts.
2. **ALWAYS** include a `negative_prompt`.
3. For **UGC-style**: mention `"shot on iPhone, slight motion blur, casual composition, imperfect framing"` in the prompt.
4. For **product shots**: specify exact material properties (`"matte packaging, glossy label, liquid inside glass bottle"`).
5. For **text/labels on products**: spell out EXACTLY what it should say.
6. For **people**: specify `"visible pores, natural skin texture, subtle blemishes"` for realism — never airbrushed plastic skin.
7. Default `negative_prompt`:
   ```
   "blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel"
   ```

---

## Step-by-Step: Brief to Prompt

### 1. Parse the Brief

Extract these elements from the user's plain-English description:

| Element | Question to Answer |
|---|---|
| Product | What is being advertised? |
| Style | Which style? (ugc-selfie, lifestyle-in-context, studio-product-hero, etc.) |
| Platform | Where will it run? Default: Facebook Feed (4:5) |
| Scene | What's happening in the image? |
| Model | Is a person shown? How are they framed? |
| Mood | What feeling should the ad evoke? |
| Lighting | What lighting setup fits the style? |
| Copy | Any text on the product label or overlay? |

If the brief is ambiguous on any element, **ask the user** before generating.

### 2. Select Defaults by Style

Apply these style-specific defaults before the user's overrides:

**ugc-selfie:**
- lighting: `ring-light`
- camera: 35mm, eye-level, medium framing, shallow DoF
- color_grading: warm
- prompt must include: "shot on iPhone, slight motion blur, casual composition, imperfect framing"
- model must include: "visible pores, natural skin texture, subtle blemishes"

**lifestyle-in-context:**
- lighting: `natural-window`
- camera: 35mm or 50mm, eye-level, medium or wide framing, moderate DoF
- color_grading: warm or neutral

**studio-product-hero:**
- lighting: `studio-softbox`
- camera: 85mm or 105mm, eye-level or high-angle, close-up framing, shallow DoF
- color_grading: neutral or cool

**flat-lay:**
- lighting: `overhead-natural`
- camera: any lens, overhead angle, wide framing, deep DoF
- color_grading: warm or vibrant

**before-after:**
- lighting: `studio-softbox` (consistent across both halves)
- camera: 50mm or 85mm, eye-level, medium framing, moderate DoF
- color_grading: neutral

**editorial-beauty:**
- lighting: `dramatic-rim`
- camera: 85mm, eye-level or low-angle, close-up framing, shallow DoF
- color_grading: cinematic

**unboxing-moment:**
- lighting: `natural-window` or `ring-light`
- camera: 35mm, eye-level or high-angle, medium framing, moderate DoF
- color_grading: warm

### 3. Build the JSON

1. Write a detailed `prompt` string that combines the scene, subject, style cues, and any required phrases from the Rules section.
2. Set `negative_prompt` — start with the default and add style-specific exclusions.
3. Fill `settings` with the camera, lighting, aspect_ratio, resolution, style, and color_grading.
4. User-specified values always override defaults.

### 4. Validate

Before saving, check:
- [ ] `aspect_ratio` matches the target platform
- [ ] `style` is one of the seven valid values
- [ ] `negative_prompt` is present (at minimum the default)
- [ ] UGC prompts include the required "shot on iPhone…" language
- [ ] People prompts include the required "visible pores…" language
- [ ] Product label text is spelled out exactly if applicable
- [ ] File name follows `{product}-{style}-{variation}.json`
- [ ] The file does not already exist (increment variation number if it does)

### 5. Save and Generate

- Save the JSON to `prompts/<category>/{filename}.json`
- Run generation
- Save the output image to `images/<category>/{filename}.png`
- Show the result to the user and ask for feedback

---

## Brand Consistency Rules

When generating multiple images for the same brand or campaign:

1. Lock `settings.lighting`, `settings.camera`, and `settings.color_grading` from the first approved image.
2. Copy those locked values into every subsequent prompt.
3. Only vary `prompt` (scene/subject description) and product-specific details.
4. If the user changes a locked field, treat that as a new visual direction and confirm before applying it to the rest of the set.

---

## Handling Feedback

When the user gives feedback on a generated image:

1. Identify which JSON fields need adjustment (e.g., "too dark" → `settings.lighting` or `settings.color_grading`).
2. Update the prompt JSON with the corrected values.
3. Save as a new variation (increment the number, never overwrite).
4. Regenerate and present the updated result.
5. If the user says "always do this", record the preference and apply it as a new default for all future prompts in this session.

---

## Example

**User brief:** "I need a Facebook ad for our vitamin C serum. Show it on a
bathroom shelf with morning light. Clean, bright, premium feel."

**Resulting prompt:**

```json
{
  "prompt": "A premium vitamin C serum in an amber glass dropper bottle with white label sitting on a white marble bathroom shelf. Soft morning sunlight streaming through a frosted window, creating gentle highlights on the glass bottle. Matte packaging, glossy label reading 'Vitamin C Brightening Serum', liquid visible inside glass bottle. Clean, bright, aspirational bathroom environment with minimal decor. Natural skin-care editorial feel.",
  "negative_prompt": "blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel, cluttered background, harsh shadows",
  "settings": {
    "resolution": "1536x1536",
    "aspect_ratio": "4:5",
    "style": "lifestyle-in-context",
    "lighting": "natural-window",
    "camera": {
      "lens": "85mm",
      "angle": "eye-level",
      "framing": "close-up",
      "height": "waist-level",
      "depth_of_field": "shallow",
      "focus": "subject"
    },
    "color_grading": "warm"
  }
}
```

**Saved to:** `prompts/lifestyle/vitamin-c-serum-bathroom-shelf-01.json`
