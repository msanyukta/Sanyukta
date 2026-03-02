# Skill: nanobanana — Ad Creative Prompt Builder

## Purpose

Turn plain-English creative briefs into structured JSON prompts optimized for
Nano Banana 2 image generation, targeting Facebook and Instagram ad placements.

---

## When to Use This Skill

Use this skill whenever the user:
- Describes an ad they want ("Show me a hero shot of…")
- Provides a creative brief for a product or campaign
- Asks for variations on an existing ad creative
- Requests a batch of assets for a campaign

---

## Prompt JSON Schema

Every prompt must follow this structure. All fields are required unless marked
optional.

```json
{
  "meta": {
    "product": "<product name, lowercase hyphenated>",
    "brand": "<brand name or 'unbranded'>",
    "category": "<one of: product-hero | lifestyle | ugc-style | before-after | infographics | social-proof>",
    "platform": "<facebook-feed | instagram-feed | stories-reels | carousel>",
    "aspect_ratio": "<4:5 | 9:16 | 1:1>"
  },
  "scene": {
    "description": "<1–2 sentence plain-English summary of the scene>",
    "setting": "<environment: studio, kitchen, bathroom, gym, desk, outdoors, etc.>",
    "time_of_day": "<morning | afternoon | golden-hour | evening | studio-lit>",
    "mood": "<clean | warm | energetic | calm | bold | minimal | luxurious>"
  },
  "subject": {
    "product_description": "<what the product looks like, packaging, color, size>",
    "product_placement": "<center | left-third | right-third | hand-held | in-use>",
    "model": "<none | hand-only | partial-body | full-body>",
    "model_description": "<optional: demographics, expression, pose — omit if model is 'none'>"
  },
  "camera": {
    "angle": "<eye-level | overhead | 45-degree | low-angle | close-up | macro>",
    "lens": "<35mm | 50mm | 85mm | 100mm-macro | 24mm-wide>",
    "depth_of_field": "<shallow | medium | deep>",
    "shot_type": "<product-closeup | medium-shot | wide-shot | flat-lay>"
  },
  "lighting": {
    "type": "<natural | studio-softbox | ring-light | golden-hour | dramatic | flat>",
    "direction": "<front | side | back | overhead | diffused>",
    "color_temperature": "<warm | neutral | cool>"
  },
  "style": {
    "color_grading": "<vibrant | muted | pastel | high-contrast | natural>",
    "texture": "<clean | film-grain | soft-glow | sharp-crisp>",
    "reference_look": "<optional: describe a visual reference, e.g. 'glossier-style minimalism'>"
  },
  "text_overlay": {
    "headline": "<optional: ad headline text to render on the image>",
    "subheadline": "<optional: secondary line of copy>",
    "cta": "<optional: call-to-action, e.g. 'Shop Now', 'Learn More'>",
    "text_placement": "<top | bottom | center | left-bar | right-bar | none>"
  },
  "negative_prompt": "<things to avoid: e.g. 'no watermarks, no borders, no extra fingers, no blurry text'>"
}
```

---

## Step-by-Step: Brief to Prompt

### 1. Parse the Brief

Extract these elements from the user's plain-English description:

| Element | Question to Answer |
|---|---|
| Product | What is being advertised? |
| Category | Which ad type? (product-hero, lifestyle, ugc-style, etc.) |
| Platform | Where will it run? Default: Facebook Feed (4:5) |
| Scene | What's happening in the image? |
| Model | Is a person shown? How much of them? |
| Mood | What feeling should the ad evoke? |
| Style | Any visual references or brand aesthetics? |
| Copy | Any text overlay needed? |

If the brief is ambiguous on any element, **ask the user** before generating.

### 2. Select Defaults by Category

Apply these category-specific defaults before the user's overrides:

**product-hero:**
- setting: studio
- camera angle: 45-degree, lens: 85mm, shallow DoF
- lighting: studio-softbox, front, neutral
- style: clean, sharp-crisp
- model: none

**lifestyle:**
- setting: contextual (kitchen, gym, desk, etc.)
- camera angle: eye-level, lens: 35mm, medium DoF
- lighting: natural, side, warm
- style: natural, vibrant
- model: partial-body or full-body

**ugc-style:**
- setting: casual real-world
- camera angle: eye-level or selfie, lens: 24mm-wide, deep DoF
- lighting: natural, diffused, warm
- style: film-grain, muted
- texture: slightly imperfect — this should look phone-shot, not polished
- model: partial-body or full-body

**before-after:**
- setting: neutral/studio or contextual
- camera angle: eye-level, lens: 50mm, medium DoF
- lighting: flat, front, neutral (consistent across both halves)
- style: high-contrast, sharp-crisp
- model: depends on product (skincare = face close-up, cleaning = wide)

**infographics:**
- setting: flat background or studio
- camera angle: overhead for flat-lay, eye-level for charts
- lighting: flat, diffused, neutral
- style: clean, vibrant, sharp-crisp
- text_overlay: required — this category always includes text

**social-proof:**
- setting: casual or neutral
- camera angle: eye-level, lens: 50mm
- lighting: natural, diffused, warm
- style: natural, soft-glow
- text_overlay: styled as a quote or review

### 3. Build the JSON

Merge user intent with category defaults. User-specified values always win.

### 4. Validate

Before saving, check:
- [ ] `aspect_ratio` matches the platform
- [ ] `category` is one of the six valid values
- [ ] `negative_prompt` is present and includes at minimum: `"no watermarks, no borders"`
- [ ] File name follows `{product}-{style}-{variation}.json`
- [ ] The file does not already exist (increment variation number if it does)

### 5. Save and Generate

- Save the JSON to `prompts/<category>/{filename}.json`
- Run generation
- Save the output image to `images/<category>/{filename}.png`
- Show the result to the user

---

## Aspect Ratio Quick Reference

| Placement | Ratio | Pixels (recommended) |
|---|---|---|
| Facebook Feed | 4:5 | 1080 x 1350 |
| Instagram Feed | 4:5 | 1080 x 1350 |
| Stories / Reels | 9:16 | 1080 x 1920 |
| Carousel | 1:1 | 1080 x 1080 |

If the user doesn't specify a platform, default to **Facebook Feed (4:5)**.

---

## Brand Consistency Rules

When generating multiple images for the same brand or campaign:

1. Lock `lighting`, `camera`, and `style` fields from the first approved image.
2. Copy those locked values into every subsequent prompt.
3. Only vary `subject`, `scene.description`, `scene.setting`, and `text_overlay`.
4. If the user changes a locked field, treat that as a new visual direction and
   confirm before applying it to the rest of the set.

---

## Handling Feedback

When the user gives feedback on a generated image:

1. Identify which JSON fields need adjustment (e.g., "too dark" → `lighting.type`,
   `lighting.direction`, or `style.color_grading`).
2. Update the prompt JSON with the corrected values.
3. Save as a new variation (increment the number, never overwrite).
4. Regenerate and present the updated result.
5. If the user says "always do this", record the preference and apply it as a
   new default for all future prompts in this session.

---

## Example

**User brief:** "I need a Facebook ad for our vitamin C serum. Show it on a
bathroom shelf with morning light. Clean, bright, premium feel."

**Resulting prompt:**

```json
{
  "meta": {
    "product": "vitamin-c-serum",
    "brand": "unbranded",
    "category": "lifestyle",
    "platform": "facebook-feed",
    "aspect_ratio": "4:5"
  },
  "scene": {
    "description": "A vitamin C serum bottle on a white marble bathroom shelf with soft morning sunlight streaming through a window.",
    "setting": "bathroom",
    "time_of_day": "morning",
    "mood": "clean"
  },
  "subject": {
    "product_description": "Amber glass dropper bottle with white label, vitamin C serum, 30ml",
    "product_placement": "center",
    "model": "none"
  },
  "camera": {
    "angle": "45-degree",
    "lens": "85mm",
    "depth_of_field": "shallow",
    "shot_type": "product-closeup"
  },
  "lighting": {
    "type": "natural",
    "direction": "side",
    "color_temperature": "warm"
  },
  "style": {
    "color_grading": "vibrant",
    "texture": "sharp-crisp",
    "reference_look": "premium skincare editorial"
  },
  "text_overlay": {
    "text_placement": "none"
  },
  "negative_prompt": "no watermarks, no borders, no text, no blurry areas, no artificial-looking lighting"
}
```

**Saved to:** `prompts/lifestyle/vitamin-c-serum-bathroom-shelf-01.json`
