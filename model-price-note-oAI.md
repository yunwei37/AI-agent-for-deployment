# Summary of Models: Behavior, Usage, Latency, and Pricing

## **GPT-4o**

- **Behavior**: Most advanced multimodal model with strong vision capabilities, 128K context.
- **Usage**: Faster, cheaper than GPT-4 Turbo; suitable for text, vision tasks, and advanced use cases.
- **Latency**: Optimized for low-latency performance.
- **Pricing**:
  - Input Tokens: $2.50 / 1M ($1.25 cached or via Batch API)
  - Output Tokens: $10.00 / 1M ($5.00 cached or via Batch API)
  - **Special Variants**:
    - Audio Preview: $100 / 1M input, $200 / 1M output
    - Older versions maintain the same pricing.

## **GPT-4o Mini**

- **Behavior**: Cost-efficient, smaller model; vision-enabled with 128K context.
- **Usage**: Designed for budget-friendly use, smarter and cheaper than GPT-3.5 Turbo.
- **Latency**: Lower resource requirements, optimized for quick results.
- **Pricing**:
  - Input Tokens: $0.15 / 1M ($0.075 cached or via Batch API)
  - Output Tokens: $0.60 / 1M ($0.30 cached or via Batch API)

## **OpenAI o1-preview**

- **Behavior**: Advanced reasoning model for complex tasks, 128K context.
- **Usage**: Designed for complex reasoning and decision-making tasks.
- **Latency**: Higher due to complex reasoning.
- **Pricing**:
  - Input Tokens: $15.00 / 1M ($7.50 cached)
  - Output Tokens: $60.00 / 1M
  - Note: Includes internal reasoning tokens not visible in API responses.

## **OpenAI o1-mini**

- **Behavior**: Fast, cost-efficient reasoning model optimized for coding, math, and science tasks, 128K context.
- **Usage**: Tailored for technical use cases requiring advanced reasoning.
- **Latency**: Faster compared to o1-preview due to simpler architecture.
- **Pricing**:
  - Input Tokens: $3.00 / 1M ($1.50 cached)
  - Output Tokens: $12.00 / 1M

### General Notes

- **Batch API**: 50% discount for batched requests; responses returned within 24 hours.
- **Prompt Caching**: Cached prompts cost 50% less than uncached.
- **Audio Costs**: $100 / 1M input tokens, $200 / 1M output tokens for audio tasks.
