/**
 * Newsletter Schema Definitions
 *
 * Zod schemas for type-safe video newsletter props.
 * Use these schemas when registering compositions in Root.tsx.
 */

import { z } from "zod";
import { zColor } from "@remotion/zod-types";

// Source reference
export const sourceSchema = z.object({
  name: z.string().describe("Source name (e.g., 'TechCrunch', 'Reuters')"),
  url: z.string().url().describe("Source URL"),
});

// Individual content section
export const sectionSchema = z.object({
  headline: z.string().min(1).max(200).describe("Section headline (max 200 chars)"),
  keyPoints: z
    .array(z.string().min(1).max(300))
    .min(1)
    .max(5)
    .describe("Key points for this section (1-5 items, max 300 chars each)"),
  imageUrl: z.string().url().optional().describe("Optional background image URL for visual style"),
  emphasis: z
    .enum(["high", "medium", "low"])
    .default("medium")
    .describe("Visual emphasis level for this section"),
});

// Color scheme preset
export const colorSchemeSchema = z.enum([
  "blue",      // Professional Blue
  "green",     // Tech Green
  "purple",    // Creative Purple
  "orange",    // Warm Orange
  "neutral",   // Neutral Dark
  "light",     // Light Mode
]).default("blue");

// Newsletter style
export const styleSchema = z.enum([
  "news-summary",         // Text-focused, professional
  "visual-presentation",  // Image-heavy, dynamic
]).default("news-summary");

// Main newsletter props schema
export const newsletterPropsSchema = z.object({
  // Content
  topic: z.string().min(1).max(100).describe("Newsletter topic/title"),
  subtitle: z.string().max(200).optional().describe("Optional subtitle"),
  sections: z
    .array(sectionSchema)
    .min(1)
    .max(10)
    .describe("Content sections (1-10)"),
  sources: z.array(sourceSchema).describe("List of sources for attribution"),

  // Styling
  style: styleSchema,
  primaryColor: zColor().describe("Primary accent color"),
  secondaryColor: zColor().describe("Secondary/gradient color"),
  backgroundColor: zColor().default("#1E293B").describe("Background color"),
  textColor: zColor().default("#F8FAFC").describe("Main text color"),

  // Timing (frames at 30fps)
  titleDurationFrames: z.number().int().positive().default(90).describe("Title card duration"),
  slideDurationFrames: z.number().int().positive().default(150).describe("Each content slide duration"),
  transitionDurationFrames: z.number().int().positive().default(30).describe("Transition duration"),
  outroDurationFrames: z.number().int().positive().default(90).describe("Outro duration"),
});

// Infer TypeScript type from schema
export type NewsletterProps = z.infer<typeof newsletterPropsSchema>;
export type Section = z.infer<typeof sectionSchema>;
export type Source = z.infer<typeof sourceSchema>;

// Helper to calculate total duration
export const calculateTotalDuration = (props: NewsletterProps): number => {
  const {
    sections,
    titleDurationFrames = 90,
    slideDurationFrames = 150,
    transitionDurationFrames = 30,
    outroDurationFrames = 90,
  } = props;

  // Title + (sections * slide) + ((sections + 1) * transition) + outro
  return (
    titleDurationFrames +
    sections.length * slideDurationFrames +
    (sections.length + 1) * transitionDurationFrames +
    outroDurationFrames
  );
};

// Default props for quick testing
export const defaultNewsletterProps: NewsletterProps = {
  topic: "Weekly Tech News",
  subtitle: "Your weekly roundup of technology updates",
  sections: [
    {
      headline: "AI Continues to Transform Industries",
      keyPoints: [
        "New language models show improved reasoning capabilities",
        "Healthcare sector adopts AI for diagnosis assistance",
        "Regulatory frameworks being developed worldwide",
      ],
      emphasis: "high",
    },
    {
      headline: "Cloud Computing Growth Accelerates",
      keyPoints: [
        "Major providers report record quarterly growth",
        "Edge computing gains momentum in IoT applications",
        "Sustainability initiatives drive green data center adoption",
      ],
      emphasis: "medium",
    },
    {
      headline: "Cybersecurity Remains Top Priority",
      keyPoints: [
        "Zero-trust architecture becomes industry standard",
        "AI-powered threat detection sees widespread deployment",
        "Organizations increase security budgets significantly",
      ],
      emphasis: "medium",
    },
  ],
  sources: [
    { name: "TechCrunch", url: "https://techcrunch.com" },
    { name: "Wired", url: "https://wired.com" },
    { name: "The Verge", url: "https://theverge.com" },
  ],
  style: "news-summary",
  primaryColor: "#2563EB",
  secondaryColor: "#60A5FA",
  backgroundColor: "#1E293B",
  textColor: "#F8FAFC",
  titleDurationFrames: 90,
  slideDurationFrames: 150,
  transitionDurationFrames: 30,
  outroDurationFrames: 90,
};

// Schema for composition registration
export const compositionSchema = newsletterPropsSchema;
