# Visual Effects Reference

Particle systems, glow effects, grain overlays, and atmospheric elements for cinematic video newsletters.

## Particle Systems

### Floating Particles

Gentle ambient particles that add depth and life to backgrounds.

```typescript
import React, { useMemo } from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, random } from "remotion";

interface Particle {
  id: number;
  x: number;
  y: number;
  size: number;
  speed: number;
  opacity: number;
  delay: number;
}

interface FloatingParticlesProps {
  count?: number;
  color?: string;
  minSize?: number;
  maxSize?: number;
  speed?: number;
}

export const FloatingParticles: React.FC<FloatingParticlesProps> = ({
  count = 50,
  color = "#FFFFFF",
  minSize = 2,
  maxSize = 6,
  speed = 0.5,
}) => {
  const frame = useCurrentFrame();
  const { width, height, durationInFrames } = useVideoConfig();

  // Generate particles once
  const particles = useMemo(() => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      x: random(`x-${i}`) * width,
      y: random(`y-${i}`) * height,
      size: minSize + random(`size-${i}`) * (maxSize - minSize),
      speed: 0.3 + random(`speed-${i}`) * speed,
      opacity: 0.2 + random(`opacity-${i}`) * 0.6,
      delay: random(`delay-${i}`) * 100,
    }));
  }, [count, width, height, minSize, maxSize, speed]);

  return (
    <AbsoluteFill style={{ overflow: "hidden", pointerEvents: "none" }}>
      {particles.map((particle) => {
        // Vertical float with slight horizontal drift
        const yOffset = ((frame + particle.delay) * particle.speed) % (height + 100);
        const xDrift = Math.sin((frame + particle.delay) * 0.02) * 30;

        // Fade particles at edges
        const edgeFade = Math.min(
          yOffset / 100,
          (height - yOffset + 100) / 100,
          1
        );

        return (
          <div
            key={particle.id}
            style={{
              position: "absolute",
              left: particle.x + xDrift,
              top: height - yOffset,
              width: particle.size,
              height: particle.size,
              borderRadius: "50%",
              backgroundColor: color,
              opacity: particle.opacity * edgeFade,
              filter: `blur(${particle.size > 4 ? 1 : 0}px)`,
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
```

### Bokeh Effect

Soft, out-of-focus light circles for depth.

```typescript
interface BokehParticle {
  x: number;
  y: number;
  size: number;
  opacity: number;
  color: string;
  pulseSpeed: number;
}

interface BokehEffectProps {
  count?: number;
  colors?: string[];
  minSize?: number;
  maxSize?: number;
}

export const BokehEffect: React.FC<BokehEffectProps> = ({
  count = 15,
  colors = ["#6366F1", "#8B5CF6", "#A855F7"],
  minSize = 40,
  maxSize = 150,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const particles = useMemo(() => {
    return Array.from({ length: count }, (_, i) => ({
      x: random(`bokeh-x-${i}`) * width,
      y: random(`bokeh-y-${i}`) * height,
      size: minSize + random(`bokeh-size-${i}`) * (maxSize - minSize),
      opacity: 0.1 + random(`bokeh-opacity-${i}`) * 0.2,
      color: colors[Math.floor(random(`bokeh-color-${i}`) * colors.length)],
      pulseSpeed: 0.02 + random(`bokeh-pulse-${i}`) * 0.03,
    }));
  }, [count, width, height, colors, minSize, maxSize]);

  return (
    <AbsoluteFill style={{ overflow: "hidden", pointerEvents: "none" }}>
      {particles.map((particle, i) => {
        const pulse = 0.8 + Math.sin(frame * particle.pulseSpeed) * 0.2;
        const drift = {
          x: Math.sin(frame * 0.01 + i) * 20,
          y: Math.cos(frame * 0.008 + i) * 15,
        };

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: particle.x + drift.x,
              top: particle.y + drift.y,
              width: particle.size * pulse,
              height: particle.size * pulse,
              borderRadius: "50%",
              background: `radial-gradient(circle, ${particle.color}40 0%, ${particle.color}00 70%)`,
              opacity: particle.opacity,
              filter: "blur(8px)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};
```

### Sparkle Effect

Twinkling points of light for magical/premium feel.

```typescript
interface SparkleEffectProps {
  count?: number;
  color?: string;
  region?: { x: number; y: number; width: number; height: number };
}

export const SparkleEffect: React.FC<SparkleEffectProps> = ({
  count = 20,
  color = "#FFFFFF",
  region,
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  const bounds = region || { x: 0, y: 0, width, height };

  const sparkles = useMemo(() => {
    return Array.from({ length: count }, (_, i) => ({
      x: bounds.x + random(`sparkle-x-${i}`) * bounds.width,
      y: bounds.y + random(`sparkle-y-${i}`) * bounds.height,
      size: 2 + random(`sparkle-size-${i}`) * 4,
      phase: random(`sparkle-phase-${i}`) * Math.PI * 2,
      speed: 0.1 + random(`sparkle-speed-${i}`) * 0.15,
      duration: 20 + random(`sparkle-dur-${i}`) * 30,
    }));
  }, [count, bounds]);

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {sparkles.map((sparkle, i) => {
        // Twinkle on/off
        const cycle = (frame * sparkle.speed + sparkle.phase) % sparkle.duration;
        const twinkle = cycle < sparkle.duration / 2
          ? cycle / (sparkle.duration / 2)
          : 1 - (cycle - sparkle.duration / 2) / (sparkle.duration / 2);

        const intensity = Math.pow(twinkle, 2);

        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: sparkle.x - sparkle.size / 2,
              top: sparkle.y - sparkle.size / 2,
              width: sparkle.size,
              height: sparkle.size,
            }}
          >
            {/* Cross shape */}
            <div
              style={{
                position: "absolute",
                left: "50%",
                top: 0,
                width: 1,
                height: "100%",
                background: color,
                opacity: intensity,
                transform: "translateX(-50%)",
                boxShadow: `0 0 ${sparkle.size * 2}px ${color}`,
              }}
            />
            <div
              style={{
                position: "absolute",
                top: "50%",
                left: 0,
                height: 1,
                width: "100%",
                background: color,
                opacity: intensity,
                transform: "translateY(-50%)",
                boxShadow: `0 0 ${sparkle.size * 2}px ${color}`,
              }}
            />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
```

## Glow Effects

### Light Bloom

Soft light emission effect for bright elements.

```typescript
interface LightBloomProps {
  color: string;
  intensity?: number;
  x?: string;
  y?: string;
  size?: number;
  animated?: boolean;
}

export const LightBloom: React.FC<LightBloomProps> = ({
  color,
  intensity = 1,
  x = "50%",
  y = "50%",
  size = 400,
  animated = true,
}) => {
  const frame = useCurrentFrame();

  const pulse = animated
    ? 0.8 + Math.sin(frame * 0.03) * 0.2
    : 1;

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div
        style={{
          position: "absolute",
          left: x,
          top: y,
          width: size * pulse,
          height: size * pulse,
          transform: "translate(-50%, -50%)",
          background: `radial-gradient(circle,
            ${color}${Math.round(intensity * 0.4 * 255).toString(16).padStart(2, '0')} 0%,
            ${color}${Math.round(intensity * 0.2 * 255).toString(16).padStart(2, '0')} 30%,
            ${color}${Math.round(intensity * 0.1 * 255).toString(16).padStart(2, '0')} 50%,
            transparent 70%
          )`,
          filter: "blur(20px)",
        }}
      />
    </AbsoluteFill>
  );
};
```

### Neon Glow Text

Text with neon light emission.

```typescript
interface NeonTextProps {
  children: React.ReactNode;
  color: string;
  intensity?: number;
  flicker?: boolean;
}

export const NeonText: React.FC<NeonTextProps> = ({
  children,
  color,
  intensity = 1,
  flicker = false,
}) => {
  const frame = useCurrentFrame();

  // Optional flicker effect
  let flickerMultiplier = 1;
  if (flicker) {
    const flickerPhase = frame % 60;
    if (flickerPhase === 15 || flickerPhase === 17) {
      flickerMultiplier = 0.7;
    } else if (flickerPhase === 45) {
      flickerMultiplier = 0.85;
    }
  }

  const glowStrength = intensity * flickerMultiplier;

  return (
    <span
      style={{
        color: "#FFFFFF",
        textShadow: `
          0 0 ${5 * glowStrength}px #FFFFFF,
          0 0 ${10 * glowStrength}px ${color},
          0 0 ${20 * glowStrength}px ${color},
          0 0 ${40 * glowStrength}px ${color},
          0 0 ${80 * glowStrength}px ${color}
        `,
      }}
    >
      {children}
    </span>
  );
};
```

### Animated Glow Border

Glowing border that animates around an element.

```typescript
interface GlowBorderProps {
  children: React.ReactNode;
  color: string;
  width?: number;
  borderRadius?: number;
  animated?: boolean;
}

export const GlowBorder: React.FC<GlowBorderProps> = ({
  children,
  color,
  width = 2,
  borderRadius = 8,
  animated = true,
}) => {
  const frame = useCurrentFrame();

  const rotation = animated ? frame * 2 : 0;

  return (
    <div
      style={{
        position: "relative",
        borderRadius,
        padding: width,
        background: `conic-gradient(from ${rotation}deg, ${color}, transparent, ${color})`,
      }}
    >
      {/* Glow layer */}
      <div
        style={{
          position: "absolute",
          inset: -width * 2,
          borderRadius: borderRadius + width,
          background: `conic-gradient(from ${rotation}deg, ${color}60, transparent, ${color}60)`,
          filter: "blur(10px)",
          zIndex: -1,
        }}
      />
      {/* Content container */}
      <div
        style={{
          borderRadius: borderRadius - width / 2,
          background: "#0A0A0F",
          position: "relative",
        }}
      >
        {children}
      </div>
    </div>
  );
};
```

## Film Effects

### Film Grain

Organic film grain overlay.

```typescript
interface FilmGrainProps {
  opacity?: number;
  speed?: number;
}

export const FilmGrain: React.FC<FilmGrainProps> = ({
  opacity = 0.05,
  speed = 1,
}) => {
  const frame = useCurrentFrame();

  // Change seed each frame for animated grain
  const seed = Math.floor(frame * speed) * 12345;

  return (
    <AbsoluteFill
      style={{
        backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' seed='${seed}' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        opacity,
        mixBlendMode: "overlay",
        pointerEvents: "none",
      }}
    />
  );
};
```

### Chromatic Aberration

RGB color separation effect.

```typescript
interface ChromaticAberrationProps {
  children: React.ReactNode;
  intensity?: number;
  animated?: boolean;
}

export const ChromaticAberration: React.FC<ChromaticAberrationProps> = ({
  children,
  intensity = 3,
  animated = false,
}) => {
  const frame = useCurrentFrame();

  const offset = animated
    ? intensity + Math.sin(frame * 0.1) * (intensity * 0.5)
    : intensity;

  return (
    <div style={{ position: "relative" }}>
      {/* Red channel - offset left */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translateX(-${offset}px)`,
          filter: "url(#red-channel)",
          mixBlendMode: "screen",
          opacity: 0.5,
        }}
      >
        {children}
      </div>
      {/* Blue channel - offset right */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          transform: `translateX(${offset}px)`,
          filter: "url(#blue-channel)",
          mixBlendMode: "screen",
          opacity: 0.5,
        }}
      >
        {children}
      </div>
      {/* Main content */}
      <div style={{ position: "relative" }}>{children}</div>

      {/* SVG filters */}
      <svg style={{ position: "absolute", width: 0, height: 0 }}>
        <defs>
          <filter id="red-channel">
            <feColorMatrix
              type="matrix"
              values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0"
            />
          </filter>
          <filter id="blue-channel">
            <feColorMatrix
              type="matrix"
              values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0"
            />
          </filter>
        </defs>
      </svg>
    </div>
  );
};
```

### Vignette

Darkened edges for focus.

```typescript
interface VignetteProps {
  intensity?: number;
  color?: string;
  size?: number;
}

export const Vignette: React.FC<VignetteProps> = ({
  intensity = 0.5,
  color = "#000000",
  size = 70,
}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse at center,
        transparent ${size - 30}%,
        ${color}${Math.round(intensity * 0.4 * 255).toString(16).padStart(2, '0')} ${size}%,
        ${color}${Math.round(intensity * 0.8 * 255).toString(16).padStart(2, '0')} 100%
      )`,
      pointerEvents: "none",
    }}
  />
);
```

### Scan Lines

CRT/retro scan line effect.

```typescript
interface ScanLinesProps {
  opacity?: number;
  lineHeight?: number;
  animated?: boolean;
}

export const ScanLines: React.FC<ScanLinesProps> = ({
  opacity = 0.1,
  lineHeight = 2,
  animated = true,
}) => {
  const frame = useCurrentFrame();
  const offset = animated ? (frame % (lineHeight * 2)) : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundImage: `repeating-linear-gradient(
          0deg,
          transparent,
          transparent ${lineHeight}px,
          rgba(0, 0, 0, ${opacity}) ${lineHeight}px,
          rgba(0, 0, 0, ${opacity}) ${lineHeight * 2}px
        )`,
        backgroundPosition: `0 ${offset}px`,
        pointerEvents: "none",
      }}
    />
  );
};
```

## Transition Effects

### Light Flash

Bright flash for dramatic transitions.

```typescript
interface LightFlashProps {
  startFrame: number;
  duration?: number;
  color?: string;
  intensity?: number;
}

export const LightFlash: React.FC<LightFlashProps> = ({
  startFrame,
  duration = 15,
  color = "#FFFFFF",
  intensity = 1,
}) => {
  const frame = useCurrentFrame();

  const progress = (frame - startFrame) / duration;
  if (progress < 0 || progress > 1) return null;

  // Quick flash in, slower fade out
  const flashCurve = progress < 0.2
    ? progress / 0.2
    : 1 - (progress - 0.2) / 0.8;

  const opacity = Math.pow(flashCurve, 2) * intensity;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: color,
        opacity,
        pointerEvents: "none",
      }}
    />
  );
};
```

### Radial Wipe

Circular reveal/hide transition.

```typescript
interface RadialWipeProps {
  progress: number;
  direction?: "in" | "out";
  centerX?: string;
  centerY?: string;
}

export const RadialWipe: React.FC<RadialWipeProps> = ({
  progress,
  direction = "in",
  centerX = "50%",
  centerY = "50%",
}) => {
  const radius = direction === "in"
    ? progress * 150
    : 150 - progress * 150;

  return (
    <AbsoluteFill
      style={{
        clipPath: `circle(${radius}% at ${centerX} ${centerY})`,
      }}
    />
  );
};
```

## Combining Effects

### Cinematic Layer Stack

Recommended layering order for effects:

```typescript
const CinematicScene: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    {/* Layer 1: Base background */}
    <AbsoluteFill style={{ backgroundColor: "#0A0A0F" }} />

    {/* Layer 2: Gradient/mesh background */}
    <MeshGradient colors={["#6366F1", "#8B5CF6", "#A855F7", "#06B6D4"]} />

    {/* Layer 3: Bokeh/particles (behind content) */}
    <BokehEffect count={10} />

    {/* Layer 4: Main content */}
    {children}

    {/* Layer 5: Floating particles (in front of content) */}
    <FloatingParticles count={30} color="#FFFFFF" />

    {/* Layer 6: Light blooms */}
    <LightBloom color="#6366F1" x="30%" y="40%" size={300} />

    {/* Layer 7: Vignette */}
    <Vignette intensity={0.4} />

    {/* Layer 8: Film grain (topmost) */}
    <FilmGrain opacity={0.03} />
  </AbsoluteFill>
);
```

### Performance Tips

1. **Limit particle count**: 30-50 for floating, 10-15 for bokeh
2. **Use `useMemo`**: Generate particle data once, not every frame
3. **Avoid filter stacking**: Multiple blurs compound performance cost
4. **Lower grain resolution**: Use smaller SVG viewBox for grain
5. **Conditional rendering**: Hide effects when not visible
6. **Test at render time**: Preview may be smoother than final render
