from src.llm_providers import AnthropicProvider

def get_llm_provider(provider_name='anthropic'):
    if provider_name == 'anthropic':
        return AnthropicProvider()
    # Add other providers here
    raise ValueError(f"Unknown LLM provider: {provider_name}")