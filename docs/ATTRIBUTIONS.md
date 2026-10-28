# Attributions and disclosure

## Competition and hardware references

- ASUS UGen AI League rules: https://contest.bhuntr.com/tw/39jg9vimiynrhlksze/home/
- ASUS UGen Intel Arc Pro B70 product page: https://www.asus.com/motherboards-components/ai-accelerator/ugen/ugen-arc-pro-b70-32g/
- ASUS B70 press release: https://press.asus.com/news/press-releases/asus-ugen-intel-arc-pro-b70-32gb-ai-accelerator/

## Candidate model references

- Qwen3-8B: https://huggingface.co/Qwen/Qwen3-8B
- Qwen2.5-VL-7B-Instruct: https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct
- Whisper: https://github.com/openai/whisper
- BAAI/bge-small-en-v1.5: https://huggingface.co/BAAI/bge-small-en-v1.5

Candidate models are not final dependencies. Exact versions will be pinned only after runtime and license validation.

## Proposal imagery

The final proposal uses slide-native diagrams and does not present a generated factory scene as evidence. The B70 product image embedded in the proposal comes from the official ASUS product page and is used for product identification in the competition proposal.

The prototype-output screen in the demo video is rendered from the repository's deterministic Stage I report and unit-test result. It is labeled as controlled synthetic data and does not present model or B70 performance.

## Video narration

- Engine: Resemble AI Chatterbox 0.1.7
- Source and license: https://github.com/resemble-ai/chatterbox (MIT)
- Voice: Chatterbox built-in reference voice; no real person's voice was cloned
- Generation: local synthesis on Apple MPS, followed by timing and loudness normalization
- Disclosure: the narration is synthetic and contains Chatterbox's built-in PerTh implicit watermark
