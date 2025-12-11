# Remotion Patterns Reference

Essential patterns for creating Remotion video newsletters.

## Core Hooks

### useCurrentFrame()
Returns the current frame number (0-indexed):
```typescript
const frame = useCurrentFrame();
// frame = 0, 1, 2, ... durationInFrames-1
```

### useVideoConfig()
Returns video configuration:
```typescript
const { fps, durationInFrames, width, height } = useVideoConfig();
// fps = 30 (typically)
// durationInFrames = total frames
// width = 1920, height = 1080 (typical)
```

## Animation Functions

### spring()
Physics-based animation (0 to 1):
```typescript
import { spring } from "remotion";

const value = spring({
  frame,                    // Current frame
  fps,                      // From useVideoConfig()
  config: {
    damping: 100,           // Higher = less bounce (10-200)
    mass: 0.5,              // Higher = slower (0.1-5)
    stiffness: 100,         // Higher = faster (10-500)
  },
});
// Returns 0 -> 1 over time
```

### interpolate()
Maps values between ranges:
```typescript
import { interpolate } from "remotion";

const opacity = interpolate(
  frame,                    // Input value
  [0, 30],                  // Input range
  [0, 1],                   // Output range
  {
    extrapolateLeft: "clamp",   // Don't go below 0
    extrapolateRight: "clamp",  // Don't go above 1
  }
);
```

## Layout Components

### AbsoluteFill
Full-screen absolutely positioned container:
```typescript
import { AbsoluteFill } from "remotion";

<AbsoluteFill style={{ backgroundColor: "white" }}>
  {/* Content fills entire frame */}
</AbsoluteFill>
```

### Sequence
Time-shifts children to start at specific frame:
```typescript
import { Sequence } from "remotion";

<Sequence from={30} durationInFrames={60}>
  {/* This component appears at frame 30 */}
  {/* Its internal frame count starts at 0 */}
</Sequence>
```

## Composition Registration

### Root.tsx Pattern
```typescript
import { Composition } from "remotion";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="CompositionName"        // Used for rendering: npx remotion render CompositionName
      component={MyComponent}     // React component
      durationInFrames={150}      // Total frames
      fps={30}                    // Frames per second
      width={1920}                // Video width
      height={1080}               // Video height
      schema={mySchema}           // Zod schema for props
      defaultProps={{             // Default values
        title: "Hello",
      }}
    />
  );
};
```

## SVG Gradient Pattern

Generate unique gradient IDs to avoid conflicts:
```typescript
import { useState } from "react";
import { random, useVideoConfig } from "remotion";

const MyComponent: React.FC = () => {
  const { width, height } = useVideoConfig();
  const [gradientId] = useState(() => String(random(null)));

  return (
    <svg viewBox={`0 0 ${width} ${height}`}>
      <defs>
        <linearGradient id={gradientId} x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="#86A8E7" />
          <stop offset="100%" stopColor="#91EAE4" />
        </linearGradient>
      </defs>
      <rect fill={`url(#${gradientId})`} width={width} height={height} />
    </svg>
  );
};
```

## Common Animation Patterns

### Fade In
```typescript
const opacity = interpolate(frame, [0, 30], [0, 1]);
```

### Fade Out at End
```typescript
const opacity = interpolate(
  frame,
  [durationInFrames - 25, durationInFrames - 15],
  [1, 0],
  { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
);
```

### Scale In with Spring
```typescript
const scale = spring({ frame, fps, config: { damping: 100 } });
<div style={{ transform: `scale(${scale})` }}>Content</div>
```

### Slide Up with Spring
```typescript
const progress = spring({ frame, fps, config: { damping: 100 } });
const translateY = interpolate(progress, [0, 1], [100, 0]);
<div style={{ transform: `translateY(${translateY}px)` }}>Content</div>
```

### Word-by-Word Animation
```typescript
const words = text.split(" ");
{words.map((word, i) => {
  const delay = i * 5; // 5 frames between words
  const scale = spring({
    fps,
    frame: frame - delay,
    config: { damping: 200 },
  });
  return (
    <span key={i} style={{ transform: `scale(${scale})`, display: "inline-block" }}>
      {word}
    </span>
  );
})}
```

### Staggered List Animation
```typescript
{items.map((item, i) => {
  const delay = i * 15; // 15 frames (0.5s) between items
  const opacity = interpolate(frame - delay, [0, 20], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const translateX = interpolate(frame - delay, [0, 20], [-50, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  return (
    <div style={{ opacity, transform: `translateX(${translateX}px)` }}>
      {item}
    </div>
  );
})}
```

## Zod Schema Patterns

### Basic Schema
```typescript
import { z } from "zod";
import { zColor } from "@remotion/zod-types";

export const mySchema = z.object({
  title: z.string(),
  color: zColor(),
  items: z.array(z.string()),
  count: z.number().min(1).max(10),
  style: z.enum(["light", "dark"]),
});

// Use with component:
export const MyComponent: React.FC<z.infer<typeof mySchema>> = (props) => {
  // props are fully typed
};
```

## CLI Commands

```bash
# Start development server
npm run dev

# Render specific composition
npx remotion render CompositionName

# Render with output path
npx remotion render CompositionName output/video.mp4

# Render with custom props
npx remotion render CompositionName --props='{"title":"Custom"}'

# Render specific frames (for testing)
npx remotion render CompositionName --frames=0-30
```
