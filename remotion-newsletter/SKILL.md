---
name: remotion-newsletter
description: Generate cinematic Remotion video newsletters and presentations with professional motion design. This skill should be used when the user asks to create a video newsletter, news summary video, topic presentation, or animated video content. It combines web research with GSAP-inspired easing curves, kinetic typography, and signature transitions for broadcast-quality output.
---

# Remotion Video Newsletter Generator

Create cinematic video newsletters with professional motion design principles inspired by GSAP, broadcast graphics, and modern editorial aesthetics.

## Motion Design Philosophy

### The 12 Principles Applied to Video

1. **Anticipation**: Elements telegraph their movement before acting (scale down before scaling up)
2. **Follow-through**: Motion continues slightly past the endpoint before settling
3. **Overlapping Action**: Different elements animate at offset timings for organic feel
4. **Slow In/Out**: Use exponential easing - never linear motion for UI elements
5. **Arcs**: Curved paths feel more natural than straight lines
6. **Secondary Action**: Supporting elements react to primary motion

### Signature Motion Identity

Every newsletter should have a recognizable motion signature:
- **Entrance pattern**: How elements first appear (reveal, morph, cascade)
- **Rhythm**: The pacing between animations (staccato, legato, syncopated)
- **Punctuation**: Distinctive micro-animations that mark transitions

## Prerequisites

- Remotion 4.x project with `remotion` in package.json
- Dependencies: `remotion`, `@remotion/zod-types`, `zod`, `react`
- Node.js 18+ environment

## Workflow

### Step 1: Understand the Creative Brief

Gather requirements with focus on aesthetic direction:

1. **Topic & Tone**: What's the subject? (tech, finance, culture, sports)
2. **Visual Style**:
   - `cinematic-dark` - Film noir, dramatic shadows, elegant reveals
   - `editorial-bold` - Magazine-style, strong typography, high contrast
   - `broadcast-news` - Professional, clean, information-dense
   - `social-native` - Punchy, vertical-friendly, attention-grabbing
3. **Duration**: Short (30s), Medium (60s), Long (90s+)
4. **Color Mood**: See `references/color-schemes.md` for cinematic palettes

### Step 2: Research & Content Architecture

Use WebSearch for 5-8 recent sources. Structure for visual storytelling:

```typescript
interface NewsletterContent {
  hook: string;              // Opening statement that grabs attention
  sections: Array<{
    headline: string;        // 5-8 words max
    subhead?: string;        // Context line
    keyPoints: string[];     // 2-3 points, 10-15 words each
    visualCue: 'stat' | 'quote' | 'comparison' | 'reveal';
    emphasis: 'hero' | 'supporting' | 'detail';
  }>;
  callback: string;          // Return to opening theme
  cta?: string;              // Call to action
}
```

### Step 3: Motion Choreography

Plan the animation sequence. See `references/motion-choreography.md` for patterns:

```
TIMELINE STRUCTURE
─────────────────────────────────────────────────────────────
0s     Title Card: Logo bloom → Title cascade → Subtitle fade
3s     Section 1:  Wipe reveal → Headline kinetic → Points stagger
8s     Transition: Morph to next context
8.5s   Section 2:  Scale in → Split headline → Points cascade
...
─────────────────────────────────────────────────────────────
```

### Step 4: Calculate Precise Timing

Use the frame calculator with 30fps base:

```typescript
// Timing constants (frames at 30fps)
const TIMING = {
  // Entrances
  quickSnap: 8,      // ~0.27s - Icon pops
  standard: 15,      // 0.5s - Text reveals
  dramatic: 30,      // 1s - Hero elements

  // Holds (reading time)
  headline: 45,      // 1.5s
  bullet: 30,        // 1s per point

  // Transitions
  microTransition: 10,  // 0.33s
  transition: 20,       // 0.67s
  sceneChange: 30,      // 1s

  // Slides
  titleCard: 90,     // 3s
  contentSlide: 150, // 5s
  outro: 90,         // 3s
};

// Calculate total duration
const calculateDuration = (sections: number) => {
  return TIMING.titleCard +
         (sections * TIMING.contentSlide) +
         ((sections + 1) * TIMING.transition) +
         TIMING.outro;
};
```

### Step 5: Generate Components

Create files in `src/Newsletter/`:

```
src/Newsletter/
├── index.tsx              # Main composition
├── TitleCard.tsx          # Cinematic opening
├── ContentSlide.tsx       # Section with kinetic type
├── TransitionSlide.tsx    # Signature transitions
├── OutroSlide.tsx         # Memorable closing
├── components/
│   ├── KineticText.tsx    # Animated typography
│   ├── RevealMask.tsx     # Clip-path reveals
│   ├── ParticleField.tsx  # Ambient particles
│   └── GlowText.tsx       # Luminous text effects
├── utils/
│   ├── easing.ts          # GSAP-style easing functions
│   └── timing.ts          # Frame calculations
└── styles/
    └── constants.ts       # Colors, fonts, spacing
```

Use templates from `assets/components/` as starting points.

### Step 6: Apply Animation Library

Reference `references/animation-library.md` for:

**GSAP-Inspired Easing** (ported for Remotion):
- `easeOutExpo` - Dramatic deceleration for reveals
- `easeInOutCubic` - Smooth transitions
- `easeOutBack` - Overshoot for emphasis
- `easeOutElastic` - Bouncy attention-grabbers

**Kinetic Typography Patterns**:
- Word-by-word reveals with stagger
- Split-text character animations
- Mask reveals (horizontal/vertical wipes)
- Scale + blur combinations

### Step 7: Register & Preview

Add to `src/Root.tsx`:

```typescript
import { Composition } from "remotion";
import { Newsletter, newsletterSchema } from "./Newsletter";

export const RemotionRoot = () => (
  <Composition
    id="Newsletter"
    component={Newsletter}
    durationInFrames={750}  // Calculated
    fps={30}
    width={1920}
    height={1080}
    schema={newsletterSchema}
    defaultProps={{
      topic: "Weekly Tech Digest",
      style: "cinematic-dark",
      // ... other props
    }}
  />
);
```

### Step 8: Render Commands

```bash
# Preview in browser
npm run dev

# Render to MP4 (H.264)
npx remotion render Newsletter out/newsletter.mp4

# Render at higher quality
npx remotion render Newsletter out/newsletter.mp4 --crf 18

# Render specific section (for testing)
npx remotion render Newsletter out/test.mp4 --frames=0-90
```

## Reference Documents

| Document | Purpose |
|----------|---------|
| `references/animation-library.md` | GSAP-inspired easing curves, motion presets |
| `references/motion-choreography.md` | Timeline patterns, stagger systems |
| `references/typography.md` | Font pairings, kinetic text techniques |
| `references/color-schemes.md` | Cinematic palettes with atmospheric depth |
| `references/visual-effects.md` | Particles, glows, grain overlays |

## Style Guidelines by Type

### Cinematic Dark
- Deep blacks with selective color accents
- Elegant serif/sans pairings (Playfair + DM Sans)
- Long easing curves (expo, cubic)
- Subtle film grain overlay
- Dramatic reveals and light blooms

### Editorial Bold
- High contrast black/white with accent color
- Strong geometric sans (Bebas Neue, Oswald)
- Snappy timing with hard cuts
- Aggressive scale animations
- Bold graphic shapes as transitions

### Broadcast News
- Professional blue/gray palette
- Clean sans-serif (Inter, Source Sans)
- Consistent moderate timing
- Lower-third graphics
- Data visualizations and charts

### Social Native
- Vibrant colors, gradients
- Rounded modern fonts (Circular, Poppins)
- Quick punchy animations
- Vertical-safe compositions (1080x1920 variant)
- Emoji and reaction elements

## Best Practices

### Performance
- Use `staticFile()` for fonts, not Google Fonts CDN
- Precompute heavy calculations outside render loop
- Limit particle count to 50-100 for smooth playback
- Use PNG sequence for complex effects

### Visual Quality
- Always clamp interpolation to avoid overshoot artifacts
- Add slight motion blur via scale/opacity for fast movements
- Use gradient meshes instead of flat backgrounds
- Apply subtle vignette for depth

### Motion Feel
- Never use linear easing for UI elements
- Stagger siblings by 3-5 frames minimum
- Hold elements in view 1.5s minimum for readability
- Exit animations should be faster than entrances (0.7x)

## Example Session

User: "Create a video newsletter about the latest developments in AI agents"

1. **Research**: Search "AI agents news December 2025"
2. **Structure**: 4 sections - Overview, Key Players, Applications, Future
3. **Style**: Editorial Bold (tech topic, high energy)
4. **Duration**: 45s (intro 3s, 4 sections × 8s, outro 3s, transitions)
5. **Generate**: Create components using templates
6. **Choreograph**: Staggered reveals, data callouts, tech-themed transitions
7. **Output**: `npx remotion render AIAgentsNewsletter`
