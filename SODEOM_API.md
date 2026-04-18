# Sodeom AI API Documentation

Free OpenAI-compatible AI API proxy via GitHub Models.

## Base URL

```
https://sodeom.com/v1
```

No API key required - pass any string as the key.

## Installation

```bash
pip install openai
```

## Basic Usage

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://sodeom.com/v1",
    api_key="any",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

## Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Count to 5"}],
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
print()
```

## Available Models

| Model | Description |
|-------|-------------|
| `gpt-4o-mini` | Default, fast and efficient |
| `gpt-4o` | Most capable GPT-4 model |
| `o1-mini` | Reasoning model |
| `Meta-Llama-3.1-8B-Instruct` | Meta's 8B instruction model |
| `Meta-Llama-3.1-70B-Instruct` | Meta's 70B instruction model |
| `Mistral-small` | Mistral's small model |
| `Phi-3.5-mini-instruct` | Microsoft's Phi-3 |

## Supported Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (default: gpt-4o-mini) |
| `messages` | array | Chat history (required) |
| `stream` | boolean | Enable SSE streaming |
| `temperature` | number | Sampling temperature (0-2) |
| `max_tokens` | integer | Max tokens (default: 1024) |
| `top_p` | number | Nucleus sampling |
| `stop` | string/array | Stop sequences |
| `frequency_penalty` | number | Frequency penalty |
| `presence_penalty` | number | Presence penalty |
| `seed` | integer | Deterministic seed |
| `n` | integer | Number of completions |

## cURL Examples

### List models

```bash
curl https://sodeom.com/v1/models
```

### Chat completion

```bash
curl https://sodeom.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Streaming

```bash
curl https://sodeom.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Count to 5"}],
    "stream": true
  }'
```

## Notes

- Requires `GITHUB_TOKEN` on the server side (handled by Sodeom)
- Free service - use responsibly
- Built by [Abdul Hadi](https://sodeom.com)