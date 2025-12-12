# Animation Library Reference

Professional motion design patterns with GSAP-inspired easing curves ported for Remotion's frame-based animation system.

## GSAP-Style Easing Functions

These easing functions accept a progress value (0-1) and return a transformed value. Use them with Remotion's `interpolate()` for professional motion.

### Easing Utility Module

Create `src/Newsletter/utils/easing.ts`:

```typescript
/**
 * GSAP-Inspired Easing Functions for Remotion
 *
 * Usage:
 * const progress = frame / duration;
 * const eased = easeOutExpo(progress);
 * const value = interpolate(eased, [0, 1], [startValue, endValue]);
 */

// ═══════════════════════════════════════════════════════════════
// EXPONENTIAL - Dramatic, cinematic feel
// ═══════════════════════════════════════════════════════════════

/** Slow start, explosive finish - great for reveals */
export const easeInExpo = (t: number): number =>
  t === 0 ? 0 : Math.pow(2, 10 * t - 10);

/** Explosive start, gentle landing - THE signature reveal ease */
export const easeOutExpo = (t: number): number =>
  t === 1 ? 1 : 1 - Math.pow(2, -10 * t);

/** Smooth acceleration/deceleration - scene transitions */
export const easeInOutExpo = (t: number): number =>
  t === 0 ? 0 :
  t === 1 ? 1 :
  t < 0.5 ? Math.pow(2, 20 * t - 10) / 2 :
  (2 - Math.pow(2, -20 * t + 10)) / 2;

// ═══════════════════════════════════════════════════════════════
// CUBIC - Professional, refined motion
// ═══════════════════════════════════════════════════════════════

/** Subtle slow start */
export const easeInCubic = (t: number): number => t * t * t;

/** Subtle deceleration - text reveals */
export const easeOutCubic = (t: number): number => 1 - Math.pow(1 - t, 3);

/** Balanced S-curve - slides, transitions */
export const easeInOutCubic = (t: number): number =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

// ═══════════════════════════════════════════════════════════════
// QUART/QUINT - More dramatic versions of cubic
// ═══════════════════════════════════════════════════════════════

export const easeOutQuart = (t: number): number => 1 - Math.pow(1 - t, 4);
export const easeOutQuint = (t: number): number => 1 - Math.pow(1 - t, 5);
export const easeInOutQuart = (t: number): number =>
  t < 0.5 ? 8 * t * t * t * t : 1 - Math.pow(-2 * t + 2, 4) / 2;

// ═══════════════════════════════════════════════════════════════
// BACK - Overshoot for emphasis and playfulness
// ═══════════════════════════════════════════════════════════════

const c1 = 1.70158;
const c2 = c1 * 1.525;
const c3 = c1 + 1;

/** Pulls back before launching forward */
export const easeInBack = (t: number): number =>
  c3 * t * t * t - c1 * t * t;

/** Overshoots then settles - buttons, icons, emphasis */
export const easeOutBack = (t: number): number =>
  1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2);

/** Pull back, overshoot, settle - dramatic entrances */
export const easeInOutBack = (t: number): number =>
  t < 0.5
    ? (Math.pow(2 * t, 2) * ((c2 + 1) * 2 * t - c2)) / 2
    : (Math.pow(2 * t - 2, 2) * ((c2 + 1) * (t * 2 - 2) + c2) + 2) / 2;

// ═══════════════════════════════════════════════════════════════
// ELASTIC - Springy, attention-grabbing
// ═══════════════════════════════════════════════════════════════

const c4 = (2 * Math.PI) / 3;
const c5 = (2 * Math.PI) / 4.5;

/** Elastic snap at end - notifications, badges */
export const easeOutElastic = (t: number): number =>
  t === 0 ? 0 :
  t === 1 ? 1 :
  Math.pow(2, -10 * t) * Math.sin((t * 10 - 0.75) * c4) + 1;

/** Full elastic motion - playful elements */
export const easeInOutElastic = (t: number): number =>
  t === 0 ? 0 :
  t === 1 ? 1 :
  t < 0.5
    ? -(Math.pow(2, 20 * t - 10) * Math.sin((20 * t - 11.125) * c5)) / 2
    : (Math.pow(2, -20 * t + 10) * Math.sin((20 * t - 11.125) * c5)) / 2 + 1;

// ═══════════════════════════════════════════════════════════════
// BOUNCE - Physical bounce effect
// ═══════════════════════════════════════════════════════════════

const n1 = 7.5625;
const d1 = 2.75;

/** Bounces at landing - physical objects */
export const easeOutBounce = (t: number): number => {
  if (t < 1 / d1) return n1 * t * t;
  if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
  if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
  return n1 * (t -= 2.625 / d1) * t + 0.984375;
};

export const easeInBounce = (t: number): number =>
  1 - easeOutBounce(1 - t);

// ═══════════════════════════════════════════════════════════════
// SINE - Gentle, organic motion
// ═══════════════════════════════════════════════════════════════

export const easeInSine = (t: number): number =>
  1 - Math.cos((t * Math.PI) / 2);

export const easeOutSine = (t: number): number =>
  Math.sin((t * Math.PI) / 2);

export const easeInOutSine = (t: number): number =>
  -(Math.cos(Math.PI * t) - 1) / 2;

// ═══════════════════════════════════════════════════════════════
// CIRC - Circular motion, smooth arcs
// ═══════════════════════════════════════════════════════════════

export const easeOutCirc = (t: number): number =>
  Math.sqrt(1 - Math.pow(t - 1, 2));

export const easeInOutCirc = (t: number): number =>
  t < 0.5
    ? (1 - Math.sqrt(1 - Math.pow(2 * t, 2))) / 2
    : (Math.sqrt(1 - Math.pow(-2 * t + 2, 2)) + 1) / 2;

// ═══════════════════════════════════════════════════════════════
// CUSTOM CUBIC BEZIER
// ═══════════════════════════════════════════════════════════════

/**
 * Custom cubic bezier easing
 * Attempt to match CSS cubic-bezier(x1, y1, x2, y2)
 */
export const cubicBezier = (
  x1: number,
  y1: number,
  x2: number,
  y2: number
) => (t: number): number => {
  // Newton-Raphson iteration to solve for parameter
  const epsilon = 1e-6;
  let guess = t;

  for (let i = 0; i < 8; i++) {
    const currentX = bezierPoint(guess, x1, x2);
    const currentSlope = bezierSlope(guess, x1, x2);

    if (Math.abs(currentX - t) < epsilon) break;
    if (Math.abs(currentSlope) < epsilon) break;

    guess -= (currentX - t) / currentSlope;
  }

  return bezierPoint(guess, y1, y2);
};

const bezierPoint = (t: number, p1: number, p2: number): number => {
  const c = 3 * p1;
  const b = 3 * (p2 - p1) - c;
  const a = 1 - c - b;
  return ((a * t + b) * t + c) * t;
};

const bezierSlope = (t: number, p1: number, p2: number): number => {
  const c = 3 * p1;
  const b = 3 * (p2 - p1) - c;
  const a = 1 - c - b;
  return (3 * a * t + 2 * b) * t + c;
};

// ═══════════════════════════════════════════════════════════════
// PRESET COMBINATIONS (Named Motion Styles)
// ═══════════════════════════════════════════════════════════════

/** Apple-style smooth motion */
export const appleEase = cubicBezier(0.25, 0.1, 0.25, 1);

/** Material Design standard */
export const materialStandard = cubicBezier(0.4, 0, 0.2, 1);

/** Material Design deceleration */
export const materialDecel = cubicBezier(0, 0, 0.2, 1);

/** Material Design acceleration */
export const materialAccel = cubicBezier(0.4, 0, 1, 1);

/** Framer Motion smooth */
export const framerSmooth = cubicBezier(0.4, 0, 0, 1);

/** Dramatic cinematic reveal */
export const cinematicReveal = cubicBezier(0.16, 1, 0.3, 1);

/** Snappy UI response */
export const snappy = cubicBezier(0.2, 0, 0, 1);
```

## Using Easing with Remotion

### Basic Pattern

```typescript
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { easeOutExpo } from "./utils/easing";

const MyComponent = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Raw progress (0 to 1)
  const progress = Math.min(frame / 30, 1); // 30-frame animation

  // Apply easing
  const easedProgress = easeOutExpo(progress);

  // Map to actual values
  const opacity = interpolate(easedProgress, [0, 1], [0, 1]);
  const translateY = interpolate(easedProgress, [0, 1], [50, 0]);
  const scale = interpolate(easedProgress, [0, 1], [0.8, 1]);

  return (
    <div style={{
      opacity,
      transform: `translateY(${translateY}px) scale(${scale})`,
    }}>
      Content
    </div>
  );
};
```

### With Delays

```typescript
const AnimatedItem = ({ index }: { index: number }) => {
  const frame = useCurrentFrame();

  // 5-frame stagger per item
  const delay = index * 5;
  const animationStart = Math.max(0, frame - delay);
  const progress = Math.min(animationStart / 20, 1);

  const easedProgress = easeOutBack(progress);

  return (
    <div style={{
      opacity: interpolate(easedProgress, [0, 1], [0, 1]),
      transform: `scale(${interpolate(easedProgress, [0, 1], [0.5, 1])})`,
    }}>
      Item {index}
    </div>
  );
};
```

## Stagger Systems

### Linear Stagger

```typescript
const STAGGER_FRAMES = 5;

{items.map((item, i) => {
  const delay = i * STAGGER_FRAMES;
  const progress = Math.min(Math.max(0, frame - delay) / 20, 1);
  const eased = easeOutExpo(progress);
  // ...
})}
```

### Exponential Stagger (Accelerating)

```typescript
{items.map((item, i) => {
  // Delays get shorter: 0, 8, 14, 18, 20, 21...
  const delay = Math.floor(20 * (1 - Math.pow(0.8, i)));
  // ...
})}
```

### Wave Stagger (Grouped)

```typescript
{items.map((item, i) => {
  // Group items in waves of 3
  const wave = Math.floor(i / 3);
  const positionInWave = i % 3;
  const delay = wave * 15 + positionInWave * 3;
  // ...
})}
```

### From-Center Stagger

```typescript
{items.map((item, i) => {
  const center = items.length / 2;
  const distanceFromCenter = Math.abs(i - center);
  const delay = distanceFromCenter * 5;
  // Center items animate first
})}
```

## Remotion Spring Configuration Presets

These map roughly to GSAP spring behaviors:

```typescript
import { spring } from "remotion";

// ═══════════════════════════════════════════════════════════════
// SPRING PRESETS
// ═══════════════════════════════════════════════════════════════

/** Snappy - Quick UI responses */
export const springSnappy = {
  damping: 200,
  mass: 0.5,
  stiffness: 200,
};

/** Smooth - Professional text reveals */
export const springSmooth = {
  damping: 100,
  mass: 1,
  stiffness: 100,
};

/** Bouncy - Playful emphasis */
export const springBouncy = {
  damping: 12,
  mass: 1,
  stiffness: 100,
};

/** Gentle - Ambient background motion */
export const springGentle = {
  damping: 100,
  mass: 3,
  stiffness: 50,
};

/** Heavy - Large graphic reveals */
export const springHeavy = {
  damping: 50,
  mass: 5,
  stiffness: 80,
};

/** Wobbly - Attention-grabbing */
export const springWobbly = {
  damping: 8,
  mass: 1,
  stiffness: 150,
};

// Usage:
const value = spring({
  frame,
  fps,
  config: springSnappy,
});
```

## Motion Patterns

### Reveal with Scale + Fade

```typescript
const RevealWithScale = () => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 25, 1);
  const eased = easeOutExpo(progress);

  return (
    <div style={{
      opacity: eased,
      transform: `scale(${0.9 + 0.1 * eased})`,
      filter: `blur(${(1 - eased) * 5}px)`,
    }}>
      Content
    </div>
  );
};
```

### Slide Up with Overshoot

```typescript
const SlideUpOvershoot = () => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 30, 1);
  const eased = easeOutBack(progress);

  return (
    <div style={{
      opacity: Math.min(progress * 2, 1), // Fade in faster
      transform: `translateY(${(1 - eased) * 60}px)`,
    }}>
      Content
    </div>
  );
};
```

### Horizontal Wipe Reveal

```typescript
const WipeReveal = () => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 20, 1);
  const eased = easeOutExpo(progress);

  return (
    <div style={{
      clipPath: `inset(0 ${(1 - eased) * 100}% 0 0)`,
    }}>
      Content that reveals from left
    </div>
  );
};
```

### Mask Reveal (Bottom to Top)

```typescript
const MaskRevealUp = () => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 25, 1);
  const eased = easeOutCubic(progress);

  return (
    <div style={{ overflow: 'hidden' }}>
      <div style={{
        transform: `translateY(${(1 - eased) * 100}%)`,
      }}>
        Content slides up into view
      </div>
    </div>
  );
};
```

### Staggered Character Animation

```typescript
const SplitText = ({ text }: { text: string }) => {
  const frame = useCurrentFrame();
  const chars = text.split('');

  return (
    <span>
      {chars.map((char, i) => {
        const delay = i * 2; // 2 frames per character
        const progress = Math.min(Math.max(0, frame - delay) / 15, 1);
        const eased = easeOutExpo(progress);

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: eased,
              transform: `translateY(${(1 - eased) * 20}px)`,
            }}
          >
            {char === ' ' ? '\u00A0' : char}
          </span>
        );
      })}
    </span>
  );
};
```

## Timing Constants

```typescript
// Frame counts at 30fps
export const TIMING = {
  // Entrance durations
  instant: 1,
  micro: 5,        // ~0.17s
  fast: 10,        // ~0.33s
  normal: 15,      // 0.5s
  moderate: 20,    // ~0.67s
  slow: 30,        // 1s
  dramatic: 45,    // 1.5s

  // Stagger intervals
  staggerTight: 3,
  staggerNormal: 5,
  staggerLoose: 8,
  staggerWide: 12,

  // Hold durations (reading time)
  holdBrief: 30,   // 1s
  holdNormal: 45,  // 1.5s
  holdLong: 60,    // 2s

  // Exit (usually faster than entrance)
  exitMultiplier: 0.7,
};
```

## Easing Selection Guide

| Context | Recommended Easing |
|---------|-------------------|
| Hero text reveal | `easeOutExpo` |
| Supporting text | `easeOutCubic` |
| Buttons/icons | `easeOutBack` |
| Scene transitions | `easeInOutCubic` |
| Emphasis moments | `easeOutElastic` |
| Background elements | `easeOutSine` |
| Notifications | `easeOutBack` + `springWobbly` |
| Data/stats | `easeOutExpo` |
| Exit animations | `easeInCubic` (faster) |
| Loops/ambient | `easeInOutSine` |
