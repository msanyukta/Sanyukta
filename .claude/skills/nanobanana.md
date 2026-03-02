# Nano Banana 2 — Ad Creative Skill

## Purpose

Convert plain-text ad creative briefs into structured JSON prompts for
Nano Banana 2 (`fal-ai/nano-banana-2`) that produce consistent, ad-ready,
realistic images for Facebook, Instagram, and e-commerce placements.

---

## When to Use This Skill

Invoke this skill whenever the user:
- Describes an ad they want ("Show me a hero shot of…")
- Provides a creative brief for a product or campaign
- Asks for variations on an existing ad creative
- Requests a batch of assets for a campaign

---

## Step-by-Step: Brief to Prompt

### 1. Parse the Brief

Extract these elements from the user's plain-English description:

| Element | Question to Answer |
|---|---|
| Product | What is being advertised? |
| Style | Which of the seven styles applies? |
| Platform | Where will it run? Default: Facebook Feed (`4:5`) |
| Scene | What's happening in the image? |
| Model | Is a person shown? How are they framed? |
| Mood | What feeling should the ad evoke? |
| Lighting | What lighting setup fits the style? |
| Copy | Any text on the product label or overlay? |

If the brief is ambiguous on **any** element, **ask the user before proceeding**.
Never guess a brand's visual style.

### 2. Select Defaults by Style

Apply style-specific defaults first, then apply any user overrides on top.

**`ugc-selfie`**
- lighting: `ring-light`
- camera: `35mm`, `eye-level`, `medium` framing, `shallow` DoF
- color_grading: `warm`
- prompt **must** include: `"shot on iPhone, slight motion blur, casual composition, imperfect framing"`
- people **must** include: `"visible pores, natural skin texture, subtle blemishes"`

**`lifestyle-in-context`**
- lighting: `natural-window`
- camera: `35mm` or `50mm`, `eye-level`, `medium` or `wide` framing, `moderate` DoF
- color_grading: `warm` or `neutral`

**`studio-product-hero`**
- lighting: `studio-softbox`
- camera: `85mm` or `105mm`, `eye-level` or `high-angle`, `close-up` framing, `shallow` DoF
- color_grading: `neutral` or `cool`

**`flat-lay`**
- lighting: `overhead-natural`
- camera: any lens, `overhead` angle, `wide` framing, `deep` DoF
- color_grading: `warm` or `vibrant`

**`before-after`**
- lighting: `studio-softbox` (must be consistent across both halves)
- camera: `50mm` or `85mm`, `eye-level`, `medium` framing, `moderate` DoF
- color_grading: `neutral`

**`editorial-beauty`**
- lighting: `dramatic-rim`
- camera: `85mm`, `eye-level` or `low-angle`, `close-up` framing, `shallow` DoF
- color_grading: `cinematic`

**`unboxing-moment`**
- lighting: `natural-window` or `ring-light`
- camera: `35mm`, `eye-level` or `high-angle`, `medium` framing, `moderate` DoF
- color_grading: `warm`

### 3. Build the JSON

Write a detailed `prompt` string combining: scene, subject, style cues, required
phrases (see Rules), material properties, and any label text. Then fill all
`settings` fields. User-specified values always override style defaults.

### 4. Validate Before Saving

- [ ] `aspect_ratio` matches the target platform
- [ ] `style` is one of the seven valid values
- [ ] `negative_prompt` is present (at minimum the default)
- [ ] UGC prompts include `"shot on iPhone, slight motion blur, casual composition, imperfect framing"`
- [ ] People prompts include `"visible pores, natural skin texture, subtle blemishes"`
- [ ] Product label text is spelled out exactly
- [ ] Filename follows `{product}-{style}-{variation}.json`
- [ ] File does not already exist — increment variation number if needed

### 5. Save and Generate

1. Save JSON to `prompts/<category>/<filename>.json`
2. Run: `FAL_KEY=<key> python scripts/generate.py prompts/<category>/<filename>.json`
3. Rename the timestamped output and move to `images/<category>/<filename>.png`
4. Show the result and ask for feedback

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

---

## Reference Tables

### Platform Defaults

| Placement | Aspect Ratio | Resolution |
|---|---|---|
| Facebook / Instagram Feed | `4:5` | `1536x1536` |
| Stories / Reels | `9:16` | `1536x1536` |
| Carousel ads | `1:1` | `1536x1536` |
| Landing page hero | `16:9` | `2048x2048` |

Default to **Facebook Feed (`4:5`)** when the user doesn't specify a platform.

### Styles

| Style | Description |
|---|---|
| `ugc-selfie` | Shot on iPhone look. Ring light or natural window. Casual, authentic, not polished. |
| `lifestyle-in-context` | Product in a real environment — kitchen counter, bathroom shelf, gym bag, desk. |
| `studio-product-hero` | Clean white or gradient background. Perfect even lighting. Catalog ads and hero images. |
| `flat-lay` | Overhead shot. Product surrounded by complementary items. Great for carousel ads. |
| `before-after` | Split composition or side-by-side. Clear transformation. Same lighting on both sides. |
| `editorial-beauty` | High-end magazine look. Dramatic lighting. Bold composition. Premium positioning. |
| `unboxing-moment` | Hands opening a package or holding a product. Excitement and discovery. |

### Lighting

| Value | Description |
|---|---|
| `ring-light` | Even, flattering facial light. The UGC standard. Slight catchlight in eyes. |
| `natural-window` | Soft diffused daylight. Lifestyle and product shots. |
| `golden-hour` | Warm directional sunlight. Outdoor lifestyle. |
| `studio-softbox` | Controlled, even light. Product hero shots. |
| `bathroom-vanity` | Warm overhead + mirror reflection. Skincare and beauty. |
| `dramatic-rim` | Hard backlight edge. Premium and editorial. |
| `overhead-natural` | Soft top-down light. Flat lay and food. |

### Camera Lenses

| Lens | Best For | Ad Use Case |
|---|---|---|
| `24mm` | Wide environment | Lifestyle scene with full room context |
| `35mm` | Environmental portrait | UGC selfie, person + product in context |
| `50mm` | General purpose | Versatile, natural feel |
| `85mm` | Portrait | Beauty and skincare close-ups |
| `105mm` | Product detail | Texture, ingredients, label close-up |
| `200mm` | Product isolation | Product floating against blurred background |

---

## Rules

1. **ALWAYS** output structured JSON — never plain-text prompts.
2. **ALWAYS** include a `negative_prompt`.
3. For **UGC-style**: include `"shot on iPhone, slight motion blur, casual composition, imperfect framing"` in the prompt.
4. For **product shots**: specify exact material properties (`"matte packaging, glossy label, liquid inside glass bottle"`).
5. For **text on labels**: spell out EXACTLY what it should say (`"white label reading 'Vitamin C Brightening Serum'"`).
6. For **people**: include `"visible pores, natural skin texture, subtle blemishes"` — never airbrushed or plastic skin.
7. **Never overwrite** an existing file — increment the variation number.

**Default `negative_prompt`:**
```
blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel
```

---

## Brand Consistency (Campaigns)

When generating multiple images for the same brand:

1. Lock `settings.lighting`, `settings.camera`, and `settings.color_grading` from the first approved image.
2. Copy those locked values verbatim into every subsequent prompt.
3. Only vary `prompt` (scene/subject description) and product-specific details.
4. If the user changes a locked field, treat it as a new visual direction and confirm before applying across the set.

---

## Feedback Loop

When the user gives feedback on a generated image:

1. Map the feedback to specific JSON fields (e.g. "too dark" → `settings.lighting` or `settings.color_grading`).
2. Note what worked and what didn't.
3. Apply preferences to all future generations in the session.
4. Save corrected prompts as new variations — never overwrite.
5. If the user says "always do this", record it as a session-level default.

---

## Example

**Brief:** "Facebook ad for our vitamin C serum. UGC style. Woman applying it in
the bathroom mirror, morning routine feel."

```json
{
  "prompt": "Young woman in her late 20s taking a bathroom mirror selfie while applying vitamin C serum from an amber glass dropper bottle. Shot on iPhone, slight motion blur, casual composition, imperfect framing. White label on bottle reading 'Vitamin C Brightening Serum'. Morning light from window catching the golden serum drops on her cheekbone. Visible pores, natural skin texture, subtle blemishes, slightly dewy skin. Toothbrush and face wash visible on shelf, felt lived-in and real.",
  "negative_prompt": "blurry, low quality, distorted, extra fingers, extra limbs, watermark, cartoon, illustration, anime, 3d render, oversaturated, plastic skin, airbrushed, stock photo feel, professional lighting setup visible, perfect symmetry, overly posed",
  "settings": {
    "resolution": "1536x1536",
    "aspect_ratio": "4:5",
    "style": "ugc-selfie",
    "lighting": "bathroom-vanity",
    "camera": {
      "lens": "35mm",
      "angle": "eye-level",
      "framing": "medium",
      "height": "eye-level",
      "depth_of_field": "shallow",
      "focus": "subject"
    },
    "color_grading": "warm"
  }
}
```

**Saved to:** `prompts/ugc-style/vitamin-c-serum-ugc-mirror-selfie-01.json`
