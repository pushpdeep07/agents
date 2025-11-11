# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

```bash
cd salescode
pip install -r requirements.txt
```

### 2. Run the Demo

See the interruption handler in action:

```bash
python demo.py
```

This will show you how the system handles different types of speech:
- ✅ Filler words (ignored)
- ✅ Real commands (processed)
- ✅ Mixed speech (processed)
- ✅ Low confidence speech (ignored)

### 3. Run Tests

Verify everything works correctly:

```bash
python test_scenarios.py
```

Expected output: All tests should pass with ✅

### 4. Configure Your Environment

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# LiveKit Server
LIVEKIT_URL=wss://your-server.livekit.cloud
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# API Keys
OPENAI_API_KEY=sk-...
DEEPGRAM_API_KEY=...
CARTESIA_API_KEY=...

# Interruption Settings (optional - defaults shown)
IGNORED_WORDS=uh,umm,hmm,haan,um,er,ah
CONFIDENCE_THRESHOLD=0.5
```

### 5. Run the Agent

#### Option A: Console Mode (Local Testing)

```bash
python agent.py console
```

Test by speaking to your microphone. The agent will:
- Ignore "uh", "umm", "hmm" while it's speaking
- Stop when you say real words like "wait" or "stop"

#### Option B: Development Mode (With LiveKit Server)

```bash
python agent.py dev
```

Then connect using:
- [LiveKit Agents Playground](https://agents-playground.livekit.io/)
- Any LiveKit client SDK
- Your custom frontend

#### Option C: Production Mode

```bash
python agent.py start
```

## 📝 Quick Test Scenarios

Once the agent is running, try these:

| What to Say | When | Expected Result |
|-------------|------|-----------------|
| "uh" | While agent speaks | Agent continues |
| "umm" | While agent speaks | Agent continues |
| "wait" | While agent speaks | Agent stops |
| "stop" | While agent speaks | Agent stops |
| "umm okay stop" | While agent speaks | Agent stops |
| "hello" | While agent is quiet | Agent responds |

## 🔧 Customization

### Add More Filler Words

Edit `.env`:
```env
IGNORED_WORDS=uh,umm,hmm,haan,um,er,ah,like,you know
```

### Adjust Confidence Threshold

Make it more or less sensitive:
```env
CONFIDENCE_THRESHOLD=0.7  # More strict (fewer false positives)
CONFIDENCE_THRESHOLD=0.3  # More lenient (more false positives)
```

### Enable Dynamic Updates

Allow adding/removing words at runtime:
```env
ENABLE_DYNAMIC_UPDATES=true
```

## 🐛 Troubleshooting

**Problem**: Tests fail
- **Solution**: Make sure you're in the `salescode` directory

**Problem**: Agent won't start
- **Solution**: Check that all API keys are set in `.env`

**Problem**: Fillers not being filtered
- **Solution**: Check logs for "Filtered filler interruption" messages

**Problem**: Too many false interruptions
- **Solution**: Increase `CONFIDENCE_THRESHOLD` or add more words to `IGNORED_WORDS`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [LiveKit Agents documentation](https://docs.livekit.io/agents/)
- Explore the code in `interruption_handler.py` and `agent.py`
- Customize the agent's instructions in `agent.py`

## 💬 Example Conversation

```
Agent: "Hello! How can I help you today?"
User: "uh" [IGNORED - agent continues]
Agent: "I'm here to assist with any questions you might have."
User: "umm" [IGNORED - agent continues]
Agent: "Feel free to ask me anything."
User: "wait" [PROCESSED - agent stops]
Agent: [stops speaking]
User: "I have a question about your service"
Agent: "Of course! What would you like to know?"
```

## 🎯 Key Features Demonstrated

1. **Filler Filtering**: "uh", "umm", "hmm" don't interrupt
2. **Real Interruptions**: "wait", "stop" work immediately
3. **Mixed Speech**: "umm okay stop" is treated as valid
4. **Confidence Filtering**: Low confidence speech is ignored
5. **Multilingual**: Supports English and Hindi fillers

## 🏆 Success Criteria

You'll know it's working when:
- ✅ Saying "uh" while agent speaks doesn't interrupt
- ✅ Saying "wait" while agent speaks does interrupt
- ✅ All tests pass
- ✅ Demo runs without errors
- ✅ Logs show "Filtered filler interruption" messages

Happy testing! 🎉

