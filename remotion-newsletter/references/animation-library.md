# Animation Library Reference

Pre-configured animation presets for video newsletters.

## Spring Configurations

### Snappy (Quick Entrances)
Fast response, minimal overshoot. Use for UI elements, buttons, icons.
```typescript
const snappy = spring({
  frame,
  fps,
  config: {
    damping: 200,
    mass: 0.5,
    stiffness: 100,
  },
});
```

### Smooth (Title Text)
Balanced movement, professional feel. Use for headlines, main content.
```typescript
const smooth = spring({
  frame,
  fps,
  config: {
    damping: 100,
  },
});
```

### Bouncy (Emphasis)
Noticeable overshoot, playful. Use for highlights, call-to-actions.
```typescript
const bouncy = spring({
  frame,
  fps,
  config: {
    damping: 10,
    mass: 0.5,
    stiffness: 100,
  },
});
```

### Gentle (Backgrounds)
Slow, subtle movement. Use for background elements, ambient animation.
```typescript
const gentle = spring({
  frame,
  fps,
  config: {
    damping: 100,
    mass: 2,
  },
});
```

### Heavy (Large Elements)
Weighty feel, dramatic. Use for large graphics, logo reveals.
```typescript
const heavy = spring({
  frame,
  fps,
  config: {
    damping: 50,
    mass: 3,
  },
});
```

## Interpolation Presets

### Fade In (Standard)
30 frames = 1 second at 30fps
```typescript
const fadeIn = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

### Fade In (Quick)
15 frames = 0.5 seconds
```typescript
const fadeInQuick = interpolate(frame, [0, 15], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});
```

### Fade Out (End of Video)
Starts 25 frames before end, completes 15 frames before end
```typescript
const fadeOut = interpolate(
  frame,
  [durationInFrames - 25, durationInFrames - 15],
  [1, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

### Slide Up
Moves from 100px below to final position
```typescript
const slideUp = interpolate(springValue, [0, 1], [100, 0]);
// Apply: transform: `translateY(${slideUp}px)`
```

### Slide Down
Moves from 100px above to final position
```typescript
const slideDown = interpolate(springValue, [0, 1], [-100, 0]);
```

### Slide Left
Enters from right side
```typescript
const slideLeft = interpolate(springValue, [0, 1], [100, 0]);
// Apply: transform: `translateX(${slideLeft}px)`
```

### Slide Right
Enters from left side
```typescript
const slideRight = interpolate(springValue, [0, 1], [-100, 0]);
```

### Scale In
Grows from 80% to 100%
```typescript
const scaleIn = interpolate(springValue, [0, 1], [0.8, 1]);
// Apply: transform: `scale(${scaleIn})`
```

### Scale Pop
Grows from 0 with slight overshoot (use bouncy spring)
```typescript
const scalePop = interpolate(bouncySpring, [0, 1], [0, 1]);
```

### Rotation
Full 360-degree rotation over video duration
```typescript
const rotation = interpolate(frame, [0, durationInFrames], [0, 360]);
// Apply: transform: `rotate(${rotation}deg)`
```

## Stagger Patterns

### Word-by-Word (Headlines)
5 frames between each word
```typescript
const words = text.split(" ");
{words.map((word, index) => {
  const delay = index * 5;
  const scale = spring({
    fps,
    frame: frame - delay,
    config: { damping: 200 },
  });
  return (
    <span
      key={index}
      style={{
        display: "inline-block",
        marginRight: 10,
        transform: `scale(${scale})`,
      }}
    >
      {word}
    </span>
  );
})}
```

### Bullet Points (Lists)
15 frames (0.5s) between each item
```typescript
{items.map((item, index) => {
  const delay = index * 15;
  const progress = spring({
    fps,
    frame: frame - delay,
    config: { damping: 100 },
  });
  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const translateX = interpolate(progress, [0, 1], [-30, 0]);

  return (
    <div
      key={index}
      style={{
        opacity,
        transform: `translateX(${translateX}px)`,
      }}
    >
      {item}
    </div>
  );
})}
```

### Cards (Grid Items)
20 frames between items, from different directions
```typescript
{cards.map((card, index) => {
  const delay = index * 20;
  const progress = spring({
    fps,
    frame: frame - delay,
    config: { damping: 100 },
  });
  const scale = interpolate(progress, [0, 1], [0.8, 1]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div
      key={index}
      style={{
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      {card}
    </div>
  );
})}
```

## Transition Presets

### Cross Fade
Two elements, one fading out while other fades in
```typescript
const transitionStart = 60; // Frame where transition starts
const transitionDuration = 30;

const outOpacity = interpolate(
  frame,
  [transitionStart, transitionStart + transitionDuration],
  [1, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);

const inOpacity = interpolate(
  frame,
  [transitionStart, transitionStart + transitionDuration],
  [0, 1],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

### Slide Transition
Current slide exits left, new slide enters from right
```typescript
const slideOutX = interpolate(progress, [0, 1], [0, -width]);
const slideInX = interpolate(progress, [0, 1], [width, 0]);
```

### Scale Transition
Current slide scales down, new slide scales up
```typescript
const scaleOut = interpolate(progress, [0, 1], [1, 0.8]);
const opacityOut = interpolate(progress, [0, 1], [1, 0]);

const scaleIn = interpolate(progress, [0, 1], [1.2, 1]);
const opacityIn = interpolate(progress, [0, 1], [0, 1]);
```

## Timing Constants

```typescript
// Standard durations (at 30fps)
const FADE_DURATION = 30;      // 1 second
const QUICK_FADE = 15;         // 0.5 seconds
const WORD_STAGGER = 5;        // 5 frames between words
const BULLET_STAGGER = 15;     // 15 frames between bullets
const CARD_STAGGER = 20;       // 20 frames between cards
const TRANSITION_DURATION = 30; // 1 second transition

// Slide durations
const TITLE_DURATION = 90;     // 3 seconds
const CONTENT_DURATION = 150;  // 5 seconds
const OUTRO_DURATION = 90;     // 3 seconds
```
