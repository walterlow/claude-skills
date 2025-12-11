---
name: remotion-newsletter
description: Generate Remotion video newsletters and presentations from web search results. This skill should be used when the user asks to create a video newsletter, news summary video, topic presentation, or animated video content about a specific subject. It performs web searches, extracts key information, and generates professional Remotion compositions with animated slides.
---

# Remotion Video Newsletter Generator

This skill enables generation of professional video newsletters and presentations from web search results using Remotion.

## Prerequisites

- Remotion 4.x project (check for `remotion` in package.json)
- Required dependencies: `remotion`, `@remotion/zod-types`, `zod`, `react`
- Node.js 18+ environment

## Workflow

### Step 1: Gather User Requirements

When the user provides a topic, clarify:
1. **Style preference**: "news-summary" (text-focused, professional) or "visual-presentation" (image-heavy, dynamic)
2. **Number of sections**: Typically 3-5 sections work best
3. **Video duration preference**: Short (30s), Medium (1min), Long (2min+)

### Step 2: Web Search and Data Collection

Use the WebSearch tool to find 5-8 recent sources on the topic:

```
WebSearch: "[topic] latest news 2025" or "[topic] updates recent"
```

From each search result, extract:
- **Headline**: The main title/finding
- **Key Points**: 2-3 important facts or insights
- **Source**: Name and URL for attribution

### Step 3: Structure the Newsletter Data

Organize search results into this structure:

```typescript
interface NewsletterData {
  topic: string;
  subtitle: string;
  style: "news-summary" | "visual-presentation";
  sections: Array<{
    headline: string;
    keyPoints: string[];
    imageUrl?: string;
    emphasis: "high" | "medium" | "low";
  }>;
  sources: Array<{
    name: string;
    url: string;
  }>;
  colorScheme: "blue" | "green" | "purple" | "orange";
}
```

### Step 4: Calculate Video Timing

Use these defaults (30fps):
- **Title Card**: 90 frames (3 seconds)
- **Content Slide**: 150 frames (5 seconds) per section
- **Transitions**: 30 frames (1 second) between slides
- **Outro**: 90 frames (3 seconds)

**Total Duration Formula**:
```
totalFrames = 90 + (sections.length * 150) + ((sections.length + 1) * 30) + 90
```

Example for 4 sections:
```
90 + (4 * 150) + (5 * 30) + 90 = 90 + 600 + 150 + 90 = 930 frames (31 seconds)
```

### Step 5: Generate Remotion Components

Create the following files in the user's Remotion project:

#### 5.1 Create Newsletter Directory
```
src/Newsletter/
  ├── index.tsx           # Main composition
  ├── TitleCard.tsx       # Opening slide
  ├── ContentSlide.tsx    # Content sections
  ├── TransitionSlide.tsx # Transitions
  ├── OutroSlide.tsx      # Closing slide
  └── constants.ts        # Colors, fonts, timing
```

#### 5.2 Generate Components Using Templates

Use the component templates in `assets/components/`:
- `TitleCard.tsx.template` - Animated title with gradient background
- `ContentSlide.tsx.template` - Headline + bullet points with staggered animation
- `TransitionSlide.tsx.template` - Smooth transitions between sections
- `OutroSlide.tsx.template` - Sources list and closing message

Read each template and customize with the newsletter data.

#### 5.3 Create the Main Composition

Generate `src/Newsletter/[TopicName]Newsletter.tsx` with:

```typescript
import { spring, AbsoluteFill, interpolate, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { z } from "zod";
import { zColor } from "@remotion/zod-types";
import { TitleCard } from "./TitleCard";
import { ContentSlide } from "./ContentSlide";
import { OutroSlide } from "./OutroSlide";

// Use the schema from assets/schemas/newsletter-schema.ts
export const newsletterSchema = z.object({
  topic: z.string(),
  sections: z.array(z.object({
    headline: z.string(),
    keyPoints: z.array(z.string()),
  })),
  primaryColor: zColor(),
  secondaryColor: zColor(),
});

export const Newsletter: React.FC<z.infer<typeof newsletterSchema>> = (props) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Fade out at end
  const opacity = interpolate(
    frame,
    [durationInFrames - 25, durationInFrames - 15],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#1E293B" }}>
      <AbsoluteFill style={{ opacity }}>
        {/* Title: frames 0-90 */}
        <Sequence from={0} durationInFrames={90}>
          <TitleCard {...props} />
        </Sequence>

        {/* Content slides with transitions */}
        {props.sections.map((section, i) => (
          <Sequence key={i} from={90 + i * 180} durationInFrames={180}>
            <ContentSlide section={section} index={i} total={props.sections.length} />
          </Sequence>
        ))}

        {/* Outro */}
        <Sequence from={90 + props.sections.length * 180}>
          <OutroSlide />
        </Sequence>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
```

### Step 6: Register Composition in Root.tsx

Add the new composition to `src/Root.tsx`:

```typescript
import { Newsletter, newsletterSchema } from "./Newsletter";

// Inside RemotionRoot:
<Composition
  id="TopicNewsletter"
  component={Newsletter}
  durationInFrames={930}  // Calculated duration
  fps={30}
  width={1920}
  height={1080}
  schema={newsletterSchema}
  defaultProps={{
    topic: "Your Topic",
    sections: [
      { headline: "...", keyPoints: ["...", "..."] },
    ],
    primaryColor: "#2563EB",
    secondaryColor: "#60A5FA",
  }}
/>
```

### Step 7: Preview and Render

Guide the user to:

1. **Preview**: `npm run dev` and select the composition in Remotion Studio
2. **Render**: `npx remotion render TopicNewsletter --output=newsletter.mp4`

## Animation Patterns Reference

See `references/animation-library.md` for:
- Spring configurations (snappy, smooth, bouncy)
- Interpolation patterns (fade in/out, slide, scale)
- Stagger timing (word-by-word, bullet points)

## Color Schemes Reference

See `references/color-schemes.md` for tested palettes:
- Professional Blue (default)
- Tech Green
- Creative Purple
- Warm Orange

## Style Guidelines

### News Summary Style
- Clean typography with large headlines
- Gradient backgrounds using SVG
- Bullet points with icons
- Minimal imagery, focus on text
- Professional, broadcast news aesthetic

### Visual Presentation Style
- Large background images (use Img from remotion)
- Overlay text with text shadows
- More dynamic animations
- Social media / magazine aesthetic

## Best Practices

1. **Always use hooks**: `useCurrentFrame()` and `useVideoConfig()` for timing
2. **Spring for entrances**: Use `spring()` with appropriate damping
3. **Interpolate for fades**: Use with `extrapolateLeft/Right: "clamp"`
4. **Unique gradient IDs**: Use `random(null)` for SVG gradient IDs
5. **Sequence for timing**: Wrap components in `<Sequence from={frame}>`
6. **AbsoluteFill for layers**: Stack elements using `<AbsoluteFill>`

## Example Usage

User: "Create a video newsletter about AI developments in 2025"

1. Search for "AI developments 2025 latest news"
2. Extract 4-5 key stories with headlines and points
3. Generate Newsletter composition with sections
4. Register in Root.tsx with calculated duration
5. Guide user to preview with `npm run dev`
