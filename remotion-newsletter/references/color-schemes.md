# Color Schemes Reference

Cinematic color palettes with atmospheric depth for broadcast-quality video newsletters.

## Color Philosophy

Great video color is about:
1. **Atmosphere** - Colors create mood before content is read
2. **Depth** - Layered tones add dimensionality
3. **Focus** - Strategic contrast guides the eye
4. **Cohesion** - Every color serves the palette

## Cinematic Palettes

### Midnight Cinema
Deep, luxurious darkness with electric accents. For: Premium content, tech reveals, noir aesthetic.

```typescript
const midnightCinema = {
  // Backgrounds (darkest to lightest)
  bg: {
    void: '#000000',        // True black for maximum contrast
    deep: '#0A0A0F',        // Near-black with blue undertone
    base: '#12121A',        // Primary background
    elevated: '#1A1A24',    // Cards, overlays
    surface: '#242430',     // Interactive elements
  },

  // Text hierarchy
  text: {
    primary: '#FFFFFF',     // Headlines
    secondary: '#E4E4E7',   // Body text
    muted: '#A1A1AA',       // Labels, captions
    subtle: '#71717A',      // Disabled, hints
  },

  // Accent colors
  accent: {
    primary: '#6366F1',     // Indigo - main accent
    secondary: '#8B5CF6',   // Violet - secondary
    glow: '#818CF8',        // Lighter for glows
  },

  // Semantic
  success: '#22C55E',
  warning: '#F59E0B',
  error: '#EF4444',

  // Gradients
  gradients: {
    hero: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%)',
    subtle: 'linear-gradient(180deg, #1A1A24 0%, #12121A 100%)',
    glow: 'radial-gradient(ellipse at center, #6366F140 0%, transparent 70%)',
  },
};
```

### Golden Hour
Warm, inviting tones inspired by sunset cinematography. For: Lifestyle, culture, human stories.

```typescript
const goldenHour = {
  bg: {
    void: '#0C0A09',
    deep: '#1C1917',
    base: '#292524',
    elevated: '#3D3835',
    surface: '#4A4541',
  },

  text: {
    primary: '#FAFAF9',
    secondary: '#E7E5E4',
    muted: '#A8A29E',
    subtle: '#78716C',
  },

  accent: {
    primary: '#F59E0B',     // Amber
    secondary: '#FB923C',   // Orange
    glow: '#FCD34D',        // Yellow for highlights
  },

  gradients: {
    hero: 'linear-gradient(135deg, #F59E0B 0%, #EA580C 50%, #DC2626 100%)',
    subtle: 'linear-gradient(180deg, #3D3835 0%, #292524 100%)',
    glow: 'radial-gradient(ellipse at center, #F59E0B30 0%, transparent 70%)',
    warmth: 'linear-gradient(to right, #FCD34D20, #F59E0B40, #EA580C20)',
  },
};
```

### Arctic Clarity
Cool, crisp blues for maximum readability. For: News, finance, data-driven content.

```typescript
const arcticClarity = {
  bg: {
    void: '#020617',        // Slate-950
    deep: '#0F172A',        // Slate-900
    base: '#1E293B',        // Slate-800
    elevated: '#334155',    // Slate-700
    surface: '#475569',     // Slate-600
  },

  text: {
    primary: '#F8FAFC',     // Slate-50
    secondary: '#E2E8F0',   // Slate-200
    muted: '#94A3B8',       // Slate-400
    subtle: '#64748B',      // Slate-500
  },

  accent: {
    primary: '#0EA5E9',     // Sky-500
    secondary: '#38BDF8',   // Sky-400
    glow: '#7DD3FC',        // Sky-300
  },

  gradients: {
    hero: 'linear-gradient(135deg, #0EA5E9 0%, #2563EB 50%, #4F46E5 100%)',
    subtle: 'linear-gradient(180deg, #334155 0%, #1E293B 100%)',
    glow: 'radial-gradient(ellipse at center, #0EA5E930 0%, transparent 70%)',
    frost: 'linear-gradient(180deg, #38BDF810 0%, transparent 50%)',
  },
};
```

### Neon Tokyo
Vibrant cyberpunk aesthetic. For: Gaming, tech culture, youth-oriented content.

```typescript
const neonTokyo = {
  bg: {
    void: '#030712',
    deep: '#0D0D1A',
    base: '#131325',
    elevated: '#1A1A35',
    surface: '#252545',
  },

  text: {
    primary: '#FFFFFF',
    secondary: '#E0E0FF',
    muted: '#9090C0',
    subtle: '#6060A0',
  },

  accent: {
    primary: '#F43F5E',     // Rose
    secondary: '#06B6D4',   // Cyan
    tertiary: '#A855F7',    // Purple
    glow: '#FB7185',
  },

  gradients: {
    hero: 'linear-gradient(135deg, #F43F5E 0%, #A855F7 50%, #06B6D4 100%)',
    neon: 'linear-gradient(90deg, #F43F5E, #A855F7, #06B6D4)',
    glow: 'radial-gradient(ellipse at center, #F43F5E40 0%, #A855F720 40%, transparent 70%)',
    scanline: 'repeating-linear-gradient(0deg, transparent, transparent 2px, #06B6D410 2px, #06B6D410 4px)',
  },
};
```

### Forest Depth
Rich, natural greens with organic warmth. For: Sustainability, health, nature content.

```typescript
const forestDepth = {
  bg: {
    void: '#022C22',
    deep: '#064E3B',
    base: '#065F46',
    elevated: '#047857',
    surface: '#059669',
  },

  text: {
    primary: '#ECFDF5',
    secondary: '#D1FAE5',
    muted: '#A7F3D0',
    subtle: '#6EE7B7',
  },

  accent: {
    primary: '#10B981',     // Emerald
    secondary: '#34D399',
    glow: '#6EE7B7',
  },

  gradients: {
    hero: 'linear-gradient(135deg, #059669 0%, #10B981 50%, #34D399 100%)',
    moss: 'linear-gradient(180deg, #065F46 0%, #022C22 100%)',
    glow: 'radial-gradient(ellipse at center, #10B98130 0%, transparent 70%)',
  },
};
```

### Editorial Monochrome
High-contrast black and white with single accent. For: Serious journalism, minimalist aesthetic.

```typescript
const editorialMono = {
  bg: {
    void: '#000000',
    deep: '#0A0A0A',
    base: '#141414',
    elevated: '#1F1F1F',
    surface: '#2A2A2A',
  },

  text: {
    primary: '#FFFFFF',
    secondary: '#D4D4D4',
    muted: '#A3A3A3',
    subtle: '#737373',
  },

  accent: {
    primary: '#EF4444',     // Single red accent
    secondary: '#F87171',
    glow: '#FCA5A5',
  },

  gradients: {
    hero: 'linear-gradient(135deg, #1F1F1F 0%, #000000 100%)',
    vignette: 'radial-gradient(ellipse at center, transparent 40%, #00000080 100%)',
    redGlow: 'radial-gradient(ellipse at center, #EF444420 0%, transparent 60%)',
  },
};
```

### Luxury Champagne
Sophisticated neutrals with gold accents. For: Premium brands, fashion, luxury.

```typescript
const luxuryChampagne = {
  bg: {
    void: '#0C0A09',
    deep: '#1C1917',
    base: '#27241D',
    elevated: '#38352D',
    surface: '#49453A',
  },

  text: {
    primary: '#FEFCE8',     // Warm white
    secondary: '#FEF9C3',
    muted: '#D4B483',
    subtle: '#A68A5B',
  },

  accent: {
    primary: '#D4AF37',     // Gold
    secondary: '#F5D061',
    glow: '#FFE066',
  },

  gradients: {
    hero: 'linear-gradient(135deg, #D4AF37 0%, #B8860B 50%, #8B6914 100%)',
    shimmer: 'linear-gradient(90deg, transparent, #D4AF3720, transparent)',
    glow: 'radial-gradient(ellipse at center, #D4AF3730 0%, transparent 60%)',
  },
};
```

## Visual Effects with Color

### Gradient Backgrounds

```typescript
// Animated gradient rotation
const AnimatedGradientBg: React.FC<{ colors: string[] }> = ({ colors }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const [gradientId] = useState(() => `grad-${random(null)}`);

  const rotation = interpolate(frame, [0, 150], [0, 360]);

  return (
    <AbsoluteFill>
      <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '100%' }}>
        <defs>
          <linearGradient
            id={gradientId}
            gradientTransform={`rotate(${rotation}, 0.5, 0.5)`}
          >
            {colors.map((color, i) => (
              <stop
                key={i}
                offset={`${(i / (colors.length - 1)) * 100}%`}
                stopColor={color}
              />
            ))}
          </linearGradient>
        </defs>
        <rect fill={`url(#${gradientId})`} width={width} height={height} />
      </svg>
    </AbsoluteFill>
  );
};
```

### Mesh Gradient

```typescript
const MeshGradient: React.FC<{
  colors: [string, string, string, string];
}> = ({ colors }) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Subtle movement
  const offset1 = Math.sin(frame * 0.02) * 5;
  const offset2 = Math.cos(frame * 0.02) * 5;

  return (
    <AbsoluteFill
      style={{
        background: `
          radial-gradient(ellipse at ${30 + offset1}% ${30 + offset2}%, ${colors[0]}60 0%, transparent 50%),
          radial-gradient(ellipse at ${70 - offset1}% ${20 + offset2}%, ${colors[1]}50 0%, transparent 50%),
          radial-gradient(ellipse at ${20 + offset2}% ${70 - offset1}%, ${colors[2]}50 0%, transparent 50%),
          radial-gradient(ellipse at ${80 - offset2}% ${80 - offset1}%, ${colors[3]}40 0%, transparent 50%),
          #0A0A0F
        `,
      }}
    />
  );
};
```

### Vignette Overlay

```typescript
const Vignette: React.FC<{
  intensity?: number;
  color?: string;
}> = ({ intensity = 0.5, color = '#000000' }) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse at center,
        transparent 30%,
        ${color}${Math.round(intensity * 0.3 * 255).toString(16).padStart(2, '0')} 70%,
        ${color}${Math.round(intensity * 0.7 * 255).toString(16).padStart(2, '0')} 100%
      )`,
      pointerEvents: 'none',
    }}
  />
);
```

### Color Pulse

```typescript
const ColorPulse: React.FC<{
  color: string;
  pulseSpeed?: number;
}> = ({ color, pulseSpeed = 0.05 }) => {
  const frame = useCurrentFrame();
  const intensity = 0.3 + Math.sin(frame * pulseSpeed) * 0.2;

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at center,
          ${color}${Math.round(intensity * 255).toString(16).padStart(2, '0')} 0%,
          transparent 70%
        )`,
        pointerEvents: 'none',
      }}
    />
  );
};
```

## Film Grain Overlay

```typescript
const FilmGrain: React.FC<{ opacity?: number }> = ({ opacity = 0.05 }) => {
  const frame = useCurrentFrame();

  // Generate pseudo-random noise pattern that changes each frame
  const seed = frame * 12345;

  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' seed='${seed}' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        opacity,
        mixBlendMode: 'overlay',
        pointerEvents: 'none',
      }}
    />
  );
};
```

## Color Transition Between Scenes

```typescript
const ColorTransition: React.FC<{
  fromColor: string;
  toColor: string;
  transitionFrame: number;
  duration?: number;
}> = ({ fromColor, toColor, transitionFrame, duration = 30 }) => {
  const frame = useCurrentFrame();

  const progress = interpolate(
    frame,
    [transitionFrame, transitionFrame + duration],
    [0, 1],
    { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }
  );

  const eased = easeInOutCubic(progress);

  // Interpolate RGB values
  const from = hexToRgb(fromColor);
  const to = hexToRgb(toColor);

  const r = Math.round(from.r + (to.r - from.r) * eased);
  const g = Math.round(from.g + (to.g - from.g) * eased);
  const b = Math.round(from.b + (to.b - from.b) * eased);

  return (
    <AbsoluteFill style={{ backgroundColor: `rgb(${r}, ${g}, ${b})` }} />
  );
};

// Helper function
const hexToRgb = (hex: string) => {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16),
  } : { r: 0, g: 0, b: 0 };
};
```

## Palette Selection Guide

| Content Type | Recommended Palette | Why |
|-------------|---------------------|-----|
| Tech/AI | Midnight Cinema | Modern, sophisticated, premium |
| Finance | Arctic Clarity | Trust, clarity, professionalism |
| Lifestyle | Golden Hour | Warmth, approachability |
| Gaming | Neon Tokyo | Energy, youth, excitement |
| Sustainability | Forest Depth | Natural, authentic |
| News | Editorial Mono | Serious, authoritative |
| Luxury | Luxury Champagne | Premium, exclusive |

## Contrast Ratios

For video accessibility, ensure text meets these minimum contrasts:

```typescript
const contrastRequirements = {
  heroText: 7.0,      // Large headlines on backgrounds
  bodyText: 4.5,      // Standard body copy
  largeText: 3.0,     // 24px+ or 19px+ bold
  uiElements: 3.0,    // Icons, borders
};

// Tested combinations (all pass 4.5:1+):
// Midnight Cinema: #FFFFFF on #12121A = 15.3:1
// Arctic Clarity: #F8FAFC on #1E293B = 12.6:1
// Golden Hour: #FAFAF9 on #292524 = 11.8:1
```
