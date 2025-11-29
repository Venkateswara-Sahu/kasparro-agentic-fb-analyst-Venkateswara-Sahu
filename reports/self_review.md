# Self-Review: Design Choices & Tradeoffs

## Agent Architecture
- **Multi-Agent Design**: Chose 5 agents for modularity and clear separation of concerns. Planner for orchestration, Data for processing, Insight for hypothesis generation, Evaluator for validation, Creative for recommendations. Tradeoff: Increased complexity vs. better reasoning flow.

## LLM Selection
- **Local Gemma 3 4B**: Prioritized for privacy and cost (no API costs). Tradeoff: Slower inference vs. full control and offline capability. Fallbacks to cloud LLMs for reliability.

## Prompt Design
- **Structured Prompts**: Used Think-Analyze-Conclude format with JSON schemas for consistency. Stored in separate .md files for reusability. Tradeoff: Verbose prompts vs. higher output quality.

## Data Handling
- **Pandas Processing**: Computed ROAS/CTR on-the-fly, grouped by date/platform. Tradeoff: Memory usage for large datasets vs. flexible summarization.

## Evaluation & Validation
- **Confidence Thresholds**: Evaluator filters insights >0.6 confidence. Tradeoff: Potential missed insights vs. quality control.

## Observability
- **JSON Logs**: Simple logging to files. Tradeoff: No real-time dashboard vs. lightweight and portable.

## Testing
- **Unit Tests**: Focused on evaluator logic. Tradeoff: Limited coverage vs. core validation.

## Tradeoffs Summary
- **Speed vs. Quality**: Local LLM is slower but private; prompts are detailed for accuracy.
- **Simplicity vs. Features**: No UI/dashboard to focus on core agentic logic.
- **Reproducibility**: Seeded randomness, pinned deps, config flags for data switching.