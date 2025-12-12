# Typography Reference

Distinctive typography choices and kinetic text techniques for broadcast-quality video newsletters.

## Font Pairing Philosophy

Great video typography follows these principles:
1. **Contrast**: Pair opposites - geometric with organic, heavy with light
2. **Hierarchy**: Display font for impact, text font for readability
3. **Character**: Fonts should have personality, not be invisible
4. **Video-Safe**: High x-height, clear letterforms, works at 1080p

## Premium Font Pairings

### Cinematic Elegance
For film-noir, documentary, prestige content.

```typescript
const cinematicElegance = {
  display: {
    family: '"Playfair Display", Georgia, serif',
    weights: [400, 700],
    usage: 'Headlines, titles, pull quotes',
  },
  body: {
    family: '"DM Sans", "Helvetica Neue", sans-serif',
    weights: [400, 500, 700],
    usage: 'Body text, bullets, labels',
  },
  accent: {
    family: '"JetBrains Mono", "Fira Code", monospace',
    weights: [400],
    usage: 'Data, statistics, timestamps',
  },
};
```

**CSS Variables:**
```css
:root {
  --font-display: 'Playfair Display', Georgia, serif;
  --font-body: 'DM Sans', 'Helvetica Neue', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### Editorial Impact
For news, tech, business content with authority.

```typescript
const editorialImpact = {
  display: {
    family: '"Bebas Neue", "Anton", sans-serif',
    weights: [400],
    usage: 'Headlines, section titles - ALL CAPS works well',
  },
  body: {
    family: '"Source Sans 3", "Open Sans", sans-serif',
    weights: [400, 600, 700],
    usage: 'Body text, detailed content',
  },
  accent: {
    family: '"Space Mono", monospace',
    weights: [400, 700],
    usage: 'Callouts, data points',
  },
};
```

### Modern Tech
For startups, AI, innovation content.

```typescript
const modernTech = {
  display: {
    family: '"Syne", "Outfit", sans-serif',
    weights: [700, 800],
    usage: 'Headlines with personality',
  },
  body: {
    family: '"Inter", "Roboto", sans-serif',
    weights: [400, 500, 600],
    usage: 'Clean, highly readable body',
  },
  accent: {
    family: '"IBM Plex Mono", monospace',
    weights: [400, 500],
    usage: 'Code, technical data',
  },
};
```

### Playful Energy
For social media, entertainment, lifestyle.

```typescript
const playfulEnergy = {
  display: {
    family: '"Clash Display", "Urbanist", sans-serif',
    weights: [600, 700],
    usage: 'Bold, friendly headlines',
  },
  body: {
    family: '"Plus Jakarta Sans", "Nunito", sans-serif',
    weights: [400, 500, 700],
    usage: 'Warm, approachable body text',
  },
  accent: {
    family: '"Familjen Grotesk", sans-serif',
    weights: [400, 600],
    usage: 'Quirky labels, tags',
  },
};
```

### Luxury Minimal
For high-end brands, fashion, architecture.

```typescript
const luxuryMinimal = {
  display: {
    family: '"Cormorant Garamond", "EB Garamond", serif',
    weights: [400, 600],
    usage: 'Elegant, refined headlines',
  },
  body: {
    family: '"Hanken Grotesk", "Archivo", sans-serif',
    weights: [300, 400, 500],
    usage: 'Light, sophisticated body',
  },
  accent: {
    family: '"Fragment Mono", monospace',
    weights: [400],
    usage: 'Minimal data display',
  },
};
```

### Brutalist Bold
For edgy, contemporary, counterculture content.

```typescript
const brutalistBold = {
  display: {
    family: '"Anybody", "Chivo", sans-serif',
    weights: [900],
    usage: 'Aggressive, statement headlines',
  },
  body: {
    family: '"Work Sans", "Karla", sans-serif',
    weights: [400, 500, 700],
    usage: 'Functional body text',
  },
  accent: {
    family: '"Victor Mono", monospace',
    weights: [400, 700],
    usage: 'Technical callouts',
  },
};
```

## Type Scale for Video

Video requires larger type than web. Here's a scale optimized for 1920x1080:

```typescript
const videoTypeScale = {
  // Headlines (display font)
  heroTitle: {
    fontSize: 120,     // Main title card
    lineHeight: 1.0,
    letterSpacing: -3,
  },
  sectionTitle: {
    fontSize: 80,      // Section headlines
    lineHeight: 1.1,
    letterSpacing: -2,
  },
  headline: {
    fontSize: 64,      // Content headlines
    lineHeight: 1.15,
    letterSpacing: -1,
  },

  // Body text (body font)
  leadText: {
    fontSize: 42,      // Important body text
    lineHeight: 1.4,
    letterSpacing: 0,
  },
  bodyLarge: {
    fontSize: 36,      // Bullet points
    lineHeight: 1.5,
    letterSpacing: 0,
  },
  bodyNormal: {
    fontSize: 28,      // Secondary text
    lineHeight: 1.5,
    letterSpacing: 0,
  },

  // Supporting (accent/mono)
  label: {
    fontSize: 20,      // Section labels
    lineHeight: 1.3,
    letterSpacing: 3,
    textTransform: 'uppercase',
  },
  caption: {
    fontSize: 18,      // Sources, timestamps
    lineHeight: 1.4,
    letterSpacing: 1,
  },
  dataPoint: {
    fontSize: 72,      // Statistics
    lineHeight: 1.0,
    letterSpacing: -2,
  },
};
```

## Loading Fonts in Remotion

### Method 1: Google Fonts (Simple, may have CORS issues)
```typescript
// In your component or Root.tsx
import { continueRender, delayRender } from 'remotion';
import { useEffect, useState } from 'react';

const useGoogleFont = (fontFamily: string) => {
  const [handle] = useState(() => delayRender());

  useEffect(() => {
    const link = document.createElement('link');
    link.href = `https://fonts.googleapis.com/css2?family=${fontFamily.replace(/ /g, '+')}:wght@400;500;600;700&display=swap`;
    link.rel = 'stylesheet';
    document.head.appendChild(link);

    link.onload = () => continueRender(handle);
    return () => document.head.removeChild(link);
  }, [fontFamily, handle]);
};
```

### Method 2: Local Fonts (Recommended for production)
```typescript
// Place font files in public/fonts/
// In src/Newsletter/styles/fonts.ts

import { staticFile } from 'remotion';

export const loadFonts = () => {
  const fonts = [
    { family: 'Playfair Display', file: 'PlayfairDisplay-Bold.woff2', weight: 700 },
    { family: 'DM Sans', file: 'DMSans-Regular.woff2', weight: 400 },
    { family: 'DM Sans', file: 'DMSans-Medium.woff2', weight: 500 },
    { family: 'DM Sans', file: 'DMSans-Bold.woff2', weight: 700 },
  ];

  fonts.forEach(({ family, file, weight }) => {
    const font = new FontFace(family, `url(${staticFile(`fonts/${file}`)})`, {
      weight: String(weight),
    });
    font.load().then(() => document.fonts.add(font));
  });
};
```

### Method 3: @remotion/google-fonts (Best)
```typescript
import { loadFont } from '@remotion/google-fonts/PlayfairDisplay';
import { loadFont as loadDMSans } from '@remotion/google-fonts/DMSans';

// In your composition
const { fontFamily: displayFont } = loadFont();
const { fontFamily: bodyFont } = loadDMSans();
```

## Kinetic Typography Patterns

### Word-by-Word Reveal

```typescript
interface WordRevealProps {
  text: string;
  staggerFrames?: number;
  animationDuration?: number;
}

const WordReveal: React.FC<WordRevealProps> = ({
  text,
  staggerFrames = 5,
  animationDuration = 20,
}) => {
  const frame = useCurrentFrame();
  const words = text.split(' ');

  return (
    <span style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3em' }}>
      {words.map((word, i) => {
        const delay = i * staggerFrames;
        const progress = Math.min(Math.max(0, frame - delay) / animationDuration, 1);
        const eased = easeOutExpo(progress);

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: eased,
              transform: `translateY(${(1 - eased) * 30}px)`,
              filter: `blur(${(1 - eased) * 4}px)`,
            }}
          >
            {word}
          </span>
        );
      })}
    </span>
  );
};
```

### Character Cascade

```typescript
const CharacterCascade: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const chars = text.split('');

  return (
    <span>
      {chars.map((char, i) => {
        const delay = i * 2;
        const progress = Math.min(Math.max(0, frame - delay) / 15, 1);
        const eased = easeOutBack(progress);

        // Random subtle rotation for organic feel
        const rotation = (Math.sin(i * 0.5) * 5) * (1 - eased);

        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: eased,
              transform: `
                translateY(${(1 - eased) * 40}px)
                rotate(${rotation}deg)
                scale(${0.5 + eased * 0.5})
              `,
              transformOrigin: 'center bottom',
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

### Typewriter Effect

```typescript
const Typewriter: React.FC<{
  text: string;
  charsPerSecond?: number;
  showCursor?: boolean;
}> = ({ text, charsPerSecond = 30, showCursor = true }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const charsPerFrame = charsPerSecond / fps;
  const visibleChars = Math.floor(frame * charsPerFrame);
  const displayText = text.slice(0, visibleChars);

  // Cursor blink (every 15 frames)
  const cursorVisible = Math.floor(frame / 15) % 2 === 0;

  return (
    <span>
      {displayText}
      {showCursor && visibleChars < text.length && (
        <span style={{ opacity: cursorVisible ? 1 : 0 }}>|</span>
      )}
    </span>
  );
};
```

### Mask Reveal (Line by Line)

```typescript
const MaskReveal: React.FC<{ text: string; direction?: 'up' | 'down' }> = ({
  text,
  direction = 'up',
}) => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 25, 1);
  const eased = easeOutCubic(progress);

  const translateY = direction === 'up'
    ? (1 - eased) * 100
    : -(1 - eased) * 100;

  return (
    <div style={{ overflow: 'hidden', display: 'inline-block' }}>
      <div style={{ transform: `translateY(${translateY}%)` }}>
        {text}
      </div>
    </div>
  );
};
```

### Scale-In with Blur

```typescript
const ScaleBlurReveal: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const progress = Math.min(frame / 30, 1);
  const eased = easeOutExpo(progress);

  return (
    <div
      style={{
        opacity: eased,
        transform: `scale(${0.8 + eased * 0.2})`,
        filter: `blur(${(1 - eased) * 10}px)`,
      }}
    >
      {children}
    </div>
  );
};
```

### Split & Converge

```typescript
const SplitConverge: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const midpoint = Math.floor(text.length / 2);
  const leftHalf = text.slice(0, midpoint);
  const rightHalf = text.slice(midpoint);

  const progress = Math.min(frame / 25, 1);
  const eased = easeOutExpo(progress);

  const offset = (1 - eased) * 100;

  return (
    <span style={{ display: 'inline-flex' }}>
      <span style={{
        transform: `translateX(-${offset}px)`,
        opacity: eased,
      }}>
        {leftHalf}
      </span>
      <span style={{
        transform: `translateX(${offset}px)`,
        opacity: eased,
      }}>
        {rightHalf}
      </span>
    </span>
  );
};
```

## Text Effects

### Gradient Text

```typescript
const GradientText: React.FC<{
  children: React.ReactNode;
  gradient: string;
}> = ({ children, gradient }) => (
  <span
    style={{
      background: gradient,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundClip: 'text',
    }}
  >
    {children}
  </span>
);

// Usage:
<GradientText gradient="linear-gradient(135deg, #667eea 0%, #764ba2 100%)">
  Headline
</GradientText>
```

### Glow Text

```typescript
const GlowText: React.FC<{
  children: React.ReactNode;
  color: string;
  intensity?: number;
}> = ({ children, color, intensity = 1 }) => (
  <span
    style={{
      textShadow: `
        0 0 ${10 * intensity}px ${color}80,
        0 0 ${20 * intensity}px ${color}60,
        0 0 ${40 * intensity}px ${color}40,
        0 0 ${80 * intensity}px ${color}20
      `,
    }}
  >
    {children}
  </span>
);
```

### Animated Glow

```typescript
const AnimatedGlow: React.FC<{ children: React.ReactNode; color: string }> = ({
  children,
  color,
}) => {
  const frame = useCurrentFrame();
  // Pulse between 0.7 and 1.3 intensity
  const intensity = 1 + Math.sin(frame * 0.1) * 0.3;

  return (
    <span
      style={{
        textShadow: `
          0 0 ${10 * intensity}px ${color}80,
          0 0 ${30 * intensity}px ${color}40
        `,
      }}
    >
      {children}
    </span>
  );
};
```

### Stroke Text (Outline)

```typescript
const StrokeText: React.FC<{
  children: React.ReactNode;
  strokeColor: string;
  strokeWidth?: number;
}> = ({ children, strokeColor, strokeWidth = 2 }) => (
  <span
    style={{
      WebkitTextStroke: `${strokeWidth}px ${strokeColor}`,
      color: 'transparent',
    }}
  >
    {children}
  </span>
);
```

## Typography Best Practices for Video

1. **Minimum hold time**: Text should be visible for at least 1.5 seconds
2. **Safe margins**: Keep text within 90% of frame (avoid edges)
3. **Contrast ratio**: Minimum 4.5:1 for body, 3:1 for large text
4. **Line length**: Max 50-60 characters per line
5. **Animation timing**: Entrance should complete before reading begins
6. **Exit timing**: Exit animations should be 30% faster than entrances
7. **Font weight**: Use 500+ weight for video (regular often looks thin)
8. **Letter-spacing**: Negative for large headlines, positive for labels
