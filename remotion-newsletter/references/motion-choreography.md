# Motion Choreography Reference

Orchestrating animations into cohesive sequences for professional video newsletters.

## The Art of Choreography

Motion choreography treats animation like music - it has rhythm, pacing, crescendos, and rests. Great video motion:

1. **Tells a story** through the sequence of reveals
2. **Guides the eye** to important information
3. **Creates anticipation** before key moments
4. **Provides breathing room** between movements

## Timeline Architecture

### Basic Structure

```
┌──────────────────────────────────────────────────────────────────┐
│ SCENE: Title Card (3 seconds = 90 frames @ 30fps)                │
├──────────────────────────────────────────────────────────────────┤
│ 0───────15──────30──────45──────60──────75──────90              │
│ │        │       │       │       │       │       │              │
│ │  BG    │       │       │       │       │       │              │
│ │  fade  │       │       │       │       │       │              │
│ │   in   │       │       │       │       │       │              │
│ │        │ TITLE │       │       │       │       │              │
│ │        │ words │       │       │       │       │              │
│ │        │ cascade       │       │       │       │              │
│ │        │       │ SUB   │       │       │       │              │
│ │        │       │ fade  │       │       │       │              │
│ │        │       │       │ LINE  │       │       │              │
│ │        │       │       │ grow  │       │       │              │
│ │        │       │       │       │ HOLD  │ fade  │              │
│ │        │       │       │       │       │  out  │              │
└──────────────────────────────────────────────────────────────────┘
```

### Sequence Building Blocks

```typescript
interface AnimationSequence {
  name: string;
  elements: Array<{
    id: string;
    startFrame: number;
    duration: number;
    animation: 'fadeIn' | 'slideUp' | 'scaleIn' | 'wipeReveal' | 'typewriter';
    easing: string;
  }>;
}

// Example: Title Card sequence
const titleCardSequence: AnimationSequence = {
  name: 'TitleCard',
  elements: [
    { id: 'background', startFrame: 0, duration: 20, animation: 'fadeIn', easing: 'easeOutSine' },
    { id: 'titleWord1', startFrame: 10, duration: 20, animation: 'scaleIn', easing: 'easeOutExpo' },
    { id: 'titleWord2', startFrame: 15, duration: 20, animation: 'scaleIn', easing: 'easeOutExpo' },
    { id: 'titleWord3', startFrame: 20, duration: 20, animation: 'scaleIn', easing: 'easeOutExpo' },
    { id: 'subtitle', startFrame: 35, duration: 25, animation: 'fadeIn', easing: 'easeOutCubic' },
    { id: 'decorLine', startFrame: 45, duration: 20, animation: 'wipeReveal', easing: 'easeOutExpo' },
  ],
};
```

## Rhythm Patterns

### Staccato (Punchy, Energetic)
Quick, sharp movements with distinct pauses. Best for: Social media, news updates, tech reveals.

```typescript
const staccatoPattern = {
  entranceDuration: 10,    // Quick in
  holdDuration: 30,        // Clear pause
  exitDuration: 7,         // Even quicker out
  stagger: 3,              // Tight stagger
  ease: 'easeOutExpo',     // Snappy feel
};

// Timing: IN - HOLD - IN - HOLD - IN - HOLD - OUT
```

### Legato (Smooth, Flowing)
Continuous, overlapping movements. Best for: Documentaries, storytelling, emotional content.

```typescript
const legatoPattern = {
  entranceDuration: 25,    // Gentle in
  holdDuration: 45,        // Comfortable pause
  exitDuration: 20,        // Graceful out
  stagger: 8,              // Generous overlap
  ease: 'easeInOutCubic',  // Smooth curves
};

// Timing: IN---HOLD---IN---HOLD---IN---HOLD---OUT
```

### Syncopated (Unexpected, Dynamic)
Off-beat timing creates interest. Best for: Creative work, music-related, experimental.

```typescript
const syncopatedPattern = {
  // Variable timing per element
  timings: [
    { entrance: 15, hold: 20 },  // Quick
    { entrance: 8, hold: 35 },   // Snappy then long
    { entrance: 25, hold: 15 },  // Slow then quick
    { entrance: 10, hold: 25 },  // Medium
  ],
  stagger: [0, 8, 12, 25],       // Irregular stagger
};
```

### Crescendo (Building Intensity)
Animations accelerate toward a climax. Best for: Reveals, countdowns, key moments.

```typescript
const crescendoPattern = {
  staggers: [15, 12, 9, 6, 4, 3, 2, 1],  // Accelerating
  durations: [30, 25, 20, 18, 15, 12, 10, 8],
  ease: 'easeOutExpo',
};
```

## Scene Choreography Templates

### Template: Hero Reveal

```
SCENE: Hero Reveal (90 frames)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frame   Element         Animation           Easing
─────────────────────────────────────────────────────
0-20    Background      Fade in 0→1         easeOutSine
5-25    Ambient glow    Scale 0.8→1, fade   easeOutExpo
10-30   Main title      Word cascade        easeOutExpo (stagger 5)
35-55   Subtitle        Slide up + fade     easeOutCubic
45-60   Accent line     Width 0→300px       easeOutExpo
50-65   CTA element     Scale pop           easeOutBack

HOLD: frames 65-80
EXIT: frames 80-90 (fade all)
```

### Template: Content Section

```
SCENE: Content Slide (150 frames)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frame   Element         Animation           Easing
─────────────────────────────────────────────────────
0-20    Section label   Fade in             easeOutCubic
5-30    Headline        Mask reveal up      easeOutExpo
20-40   Subhead         Slide up + fade     easeOutCubic
35-55   Bullet 1        Slide right + fade  easeOutExpo
50-70   Bullet 2        Slide right + fade  easeOutExpo
65-85   Bullet 3        Slide right + fade  easeOutExpo
80-95   Visual element  Scale in            easeOutBack

HOLD: frames 95-135
EXIT: frames 135-150 (slide left, fade)
```

### Template: Data Reveal

```
SCENE: Statistics (120 frames)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frame   Element         Animation           Easing
─────────────────────────────────────────────────────
0-15    Background      Color shift         easeInOutCubic
5-35    Big number      Count up + scale    easeOutExpo
15-35   Unit label      Fade in             easeOutCubic
30-45   Context line    Typewriter          linear
40-60   Comparison bar  Width grow          easeOutExpo
55-70   Percentage      Count up            easeOutCubic

HOLD: frames 70-105
EXIT: frames 105-120
```

### Template: Scene Transition

```
SCENE: Transition (30 frames)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Frame   Element         Animation           Easing
─────────────────────────────────────────────────────
0-15    Previous scene  Scale 0.95, fade    easeInCubic
0-20    Wipe overlay    Diagonal sweep      easeInOutExpo
10-25   Color flash     Opacity pulse       easeOutSine
15-30   Next scene      Scale 1.05→1, fade  easeOutExpo
```

## Orchestration Techniques

### The "Golden Ratio" Stagger
Elements animate at 1.618x the previous delay:

```typescript
const goldenStagger = (index: number, baseDelay: number = 5) => {
  if (index === 0) return 0;
  return Math.round(baseDelay * Math.pow(1.618, index - 1));
};

// Results: 0, 5, 8, 13, 21, 34, 55...
// Creates natural, pleasing rhythm
```

### The "Cascade" Pattern
Parent triggers children in sequence:

```typescript
const CascadeContainer: React.FC<{ children: React.ReactNode[] }> = ({ children }) => {
  const frame = useCurrentFrame();

  // Container fades in first
  const containerProgress = Math.min(frame / 20, 1);
  const containerEased = easeOutCubic(containerProgress);

  return (
    <div style={{ opacity: containerEased }}>
      {React.Children.map(children, (child, i) => {
        // Children start after container is 50% visible
        const childDelay = 10 + i * 5;
        const childProgress = Math.min(Math.max(0, frame - childDelay) / 20, 1);
        const childEased = easeOutExpo(childProgress);

        return (
          <div style={{
            opacity: childEased,
            transform: `translateY(${(1 - childEased) * 20}px)`,
          }}>
            {child}
          </div>
        );
      })}
    </div>
  );
};
```

### The "Anticipation" Pattern
Small movement before main action:

```typescript
const AnticipatedReveal: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  // Phase 1: Anticipation (slight scale down)
  // Phase 2: Main action (scale up with overshoot)
  const anticipation = frame < 10
    ? interpolate(frame, [0, 10], [1, 0.95])
    : 0.95;

  const mainAction = frame >= 10
    ? easeOutBack(Math.min((frame - 10) / 20, 1))
    : 0;

  const scale = frame < 10
    ? anticipation
    : 0.95 + mainAction * 0.05;

  return (
    <div style={{ transform: `scale(${scale})` }}>
      {children}
    </div>
  );
};
```

### The "Overlap" Pattern
Next element starts before previous finishes:

```typescript
const OverlappingSequence: React.FC<{ items: string[] }> = ({ items }) => {
  const frame = useCurrentFrame();

  return (
    <>
      {items.map((item, i) => {
        // Each item takes 30 frames but starts 20 frames apart
        const startFrame = i * 20;
        const endFrame = startFrame + 30;

        const progress = interpolate(frame, [startFrame, endFrame], [0, 1], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        });

        return (
          <div key={i} style={{ opacity: easeOutCubic(progress) }}>
            {item}
          </div>
        );
      })}
    </>
  );
};
```

## Exit Choreography

Exits should be:
- **30% faster** than entrances
- **Simpler** - usually just fade or slide
- **Coordinated** - all elements exit together or in reverse order

### Simultaneous Exit

```typescript
const SimultaneousExit: React.FC<{
  children: React.ReactNode;
  exitFrame: number;
}> = ({ children, exitFrame }) => {
  const frame = useCurrentFrame();

  if (frame < exitFrame) return <>{children}</>;

  const exitProgress = Math.min((frame - exitFrame) / 15, 1);
  const eased = easeInCubic(exitProgress);

  return (
    <div style={{
      opacity: 1 - eased,
      transform: `scale(${1 - eased * 0.1})`,
    }}>
      {children}
    </div>
  );
};
```

### Reverse Cascade Exit

```typescript
const ReverseCascadeExit: React.FC<{
  items: React.ReactNode[];
  exitFrame: number;
}> = ({ items, exitFrame }) => {
  const frame = useCurrentFrame();

  return (
    <>
      {items.map((item, i) => {
        // Last item exits first
        const reverseIndex = items.length - 1 - i;
        const itemExitFrame = exitFrame + reverseIndex * 3;
        const exitProgress = Math.min(Math.max(0, frame - itemExitFrame) / 12, 1);
        const eased = easeInCubic(exitProgress);

        return (
          <div key={i} style={{
            opacity: 1 - eased,
            transform: `translateX(${eased * -30}px)`,
          }}>
            {item}
          </div>
        );
      })}
    </>
  );
};
```

## Timing Formulas

### Reading Time Calculator

```typescript
// Words per second (comfortable reading pace for video)
const WPS_SLOW = 2;      // Contemplative
const WPS_NORMAL = 3;    // Standard
const WPS_FAST = 4;      // Energetic

const calculateReadingFrames = (
  text: string,
  fps: number,
  pace: 'slow' | 'normal' | 'fast' = 'normal'
) => {
  const wps = { slow: WPS_SLOW, normal: WPS_NORMAL, fast: WPS_FAST }[pace];
  const wordCount = text.split(/\s+/).length;
  const seconds = wordCount / wps;
  return Math.ceil(seconds * fps);
};
```

### Total Scene Duration

```typescript
const calculateSceneDuration = (
  entranceFrames: number,
  holdFrames: number,
  exitFrames: number,
  buffer: number = 5  // Breathing room
) => {
  return entranceFrames + holdFrames + exitFrames + buffer;
};

// Example:
// Title entrance: 40 frames
// Title hold (readable): 50 frames
// Title exit: 15 frames
// Buffer: 5 frames
// Total: 110 frames (3.67 seconds)
```

## Motion Signature Examples

### "Apple Keynote" Style
```typescript
const appleStyle = {
  entranceEase: 'easeOutCubic',
  entranceDuration: 40,
  stagger: 8,
  movementType: 'slideUp',
  slideDistance: 60,
  initialScale: 0.98,
  blur: true,
  blurAmount: 8,
};
```

### "Netflix Trailer" Style
```typescript
const netflixStyle = {
  entranceEase: 'easeOutExpo',
  entranceDuration: 25,
  stagger: 4,
  movementType: 'scaleIn',
  initialScale: 1.2,
  dramaticPauses: true,
  pauseDuration: 30,
};
```

### "ESPN Broadcast" Style
```typescript
const espnStyle = {
  entranceEase: 'easeOutBack',
  entranceDuration: 15,
  stagger: 3,
  movementType: 'slideRight',
  overshoot: true,
  sharpCuts: true,
};
```
