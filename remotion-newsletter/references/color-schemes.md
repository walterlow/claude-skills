# Color Schemes Reference

Pre-tested color palettes for video newsletters.

## Professional Blue (Default)

Modern, trustworthy, corporate feel. Best for business news, tech updates.

```typescript
const professionalBlue = {
  primary: "#2563EB",      // Blue-600
  secondary: "#60A5FA",    // Blue-400
  background: "#1E293B",   // Slate-800
  backgroundAlt: "#0F172A", // Slate-900
  text: "#F8FAFC",         // Slate-50
  textMuted: "#94A3B8",    // Slate-400
  accent: "#3B82F6",       // Blue-500
  gradient: ["#2563EB", "#60A5FA"],
};
```

**Usage:**
```typescript
<AbsoluteFill style={{ backgroundColor: "#1E293B" }}>
  <svg>
    <linearGradient>
      <stop offset="0%" stopColor="#2563EB" />
      <stop offset="100%" stopColor="#60A5FA" />
    </linearGradient>
  </svg>
  <h1 style={{ color: "#F8FAFC" }}>Headline</h1>
  <p style={{ color: "#94A3B8" }}>Subtext</p>
</AbsoluteFill>
```

## Tech Green

Fresh, innovative, growth-oriented. Best for sustainability, health tech, startups.

```typescript
const techGreen = {
  primary: "#10B981",      // Emerald-500
  secondary: "#6EE7B7",    // Emerald-300
  background: "#064E3B",   // Emerald-900
  backgroundAlt: "#022C22", // Emerald-950
  text: "#ECFDF5",         // Emerald-50
  textMuted: "#6EE7B7",    // Emerald-300
  accent: "#34D399",       // Emerald-400
  gradient: ["#10B981", "#6EE7B7"],
};
```

## Creative Purple

Bold, imaginative, premium feel. Best for entertainment, arts, luxury brands.

```typescript
const creativePurple = {
  primary: "#8B5CF6",      // Violet-500
  secondary: "#C4B5FD",    // Violet-300
  background: "#1E1B4B",   // Indigo-950
  backgroundAlt: "#0C0A22", // Custom dark
  text: "#F5F3FF",         // Violet-50
  textMuted: "#A5B4FC",    // Indigo-300
  accent: "#A78BFA",       // Violet-400
  gradient: ["#8B5CF6", "#C4B5FD"],
};
```

## Warm Orange

Energetic, friendly, approachable. Best for food, lifestyle, community news.

```typescript
const warmOrange = {
  primary: "#F97316",      // Orange-500
  secondary: "#FDBA74",    // Orange-300
  background: "#431407",   // Orange-950
  backgroundAlt: "#1C0A02", // Custom dark
  text: "#FFF7ED",         // Orange-50
  textMuted: "#FED7AA",    // Orange-200
  accent: "#FB923C",       // Orange-400
  gradient: ["#F97316", "#FDBA74"],
};
```

## Neutral Dark

Minimal, sophisticated, content-focused. Best for serious news, documentaries.

```typescript
const neutralDark = {
  primary: "#FFFFFF",      // White
  secondary: "#A1A1AA",    // Zinc-400
  background: "#18181B",   // Zinc-900
  backgroundAlt: "#09090B", // Zinc-950
  text: "#FAFAFA",         // Zinc-50
  textMuted: "#71717A",    // Zinc-500
  accent: "#E4E4E7",       // Zinc-200
  gradient: ["#27272A", "#3F3F46"], // Zinc-800 to Zinc-700
};
```

## Light Mode

Clean, airy, accessible. Best for educational content, daytime viewing.

```typescript
const lightMode = {
  primary: "#1E293B",      // Slate-800
  secondary: "#475569",    // Slate-600
  background: "#FFFFFF",   // White
  backgroundAlt: "#F8FAFC", // Slate-50
  text: "#0F172A",         // Slate-900
  textMuted: "#64748B",    // Slate-500
  accent: "#3B82F6",       // Blue-500
  gradient: ["#E2E8F0", "#F8FAFC"], // Slate-200 to Slate-50
};
```

## Remotion Default

Based on the existing HelloWorld project colors.

```typescript
const remotionDefault = {
  primary: "#86A8E7",      // Original COLOR_1
  secondary: "#91EAE4",    // Original logoColor1
  background: "#FFFFFF",   // White
  backgroundAlt: "#F1F5F9", // Slate-100
  text: "#000000",         // Black
  textMuted: "#64748B",    // Slate-500
  accent: "#86A8E7",       // COLOR_1
  gradient: ["#86A8E7", "#91EAE4"],
};
```

## SVG Gradient Examples

### Vertical Gradient
```typescript
<linearGradient id={gradientId} x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stopColor={primary} />
  <stop offset="100%" stopColor={secondary} />
</linearGradient>
```

### Horizontal Gradient
```typescript
<linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="0%">
  <stop offset="0%" stopColor={primary} />
  <stop offset="100%" stopColor={secondary} />
</linearGradient>
```

### Diagonal Gradient
```typescript
<linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
  <stop offset="0%" stopColor={primary} />
  <stop offset="100%" stopColor={secondary} />
</linearGradient>
```

### Radial Gradient (for backgrounds)
```typescript
<radialGradient id={gradientId} cx="50%" cy="50%" r="70%">
  <stop offset="0%" stopColor={secondary} />
  <stop offset="100%" stopColor={background} />
</radialGradient>
```

## CSS Shadow Presets

### Text Shadow (Light on Dark)
```typescript
textShadow: "0 2px 10px rgba(0, 0, 0, 0.5)"
```

### Text Shadow (Glow Effect)
```typescript
textShadow: `0 0 20px ${primary}80` // 50% opacity
```

### Box Shadow (Card)
```typescript
boxShadow: "0 4px 20px rgba(0, 0, 0, 0.3)"
```

### Box Shadow (Elevated)
```typescript
boxShadow: "0 10px 40px rgba(0, 0, 0, 0.5)"
```

## Combining Colors with Animation

### Animated Gradient Background
```typescript
const gradientRotation = interpolate(frame, [0, durationInFrames], [0, 360]);

<svg style={{ transform: `rotate(${gradientRotation}deg)` }}>
  <linearGradient id={gradientId}>
    <stop offset="0%" stopColor={primary} />
    <stop offset="100%" stopColor={secondary} />
  </linearGradient>
  <rect fill={`url(#${gradientId})`} width="200%" height="200%" x="-50%" y="-50%" />
</svg>
```

### Color Fade Transition
```typescript
// Interpolate between two colors (use for background transitions)
const colorProgress = interpolate(frame, [startFrame, endFrame], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// Apply with CSS: Use two overlapping AbsoluteFills with opacity
<AbsoluteFill style={{ backgroundColor: color1, opacity: 1 - colorProgress }} />
<AbsoluteFill style={{ backgroundColor: color2, opacity: colorProgress }} />
```
