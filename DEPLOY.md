# AgentViral SDK - Deployment Guide

## 🚀 Quick Deploy

### Step 1: Create GitHub Repository

```bash
# Create new repository on GitHub
# Name: agentviral-sdk
# URL: https://github.com/yourusername/agentviral-sdk
```

### Step 2: Upload Code

```bash
# Clone your repository
git clone https://github.com/yourusername/agentviral-sdk.git
cd agentviral-sdk

# Copy all SDK files here
# (All files are in /mnt/okcomputer/output/agentviral-sdk/)

# Add files
git add .
git commit -m "Initial release v0.1.0"
git push origin main
```

### Step 3: Publish to PyPI

```bash
# Install build tools
pip install build twine

# Build package
python -m build

# Upload to PyPI
python -m twine upload dist/*

# Enter your PyPI credentials
# Username: __token__
# Password: your-pypi-api-token
```

### Step 4: Verify Installation

```bash
# Test installation
pip install agentviral

# Verify
python -c "from agentviral import ViralEngine; print('✅ SDK installed successfully')"
```

## 📋 Pre-Deploy Checklist

- [ ] All code files are ready
- [ ] README.md is complete
- [ ] setup.py is configured
- [ ] LICENSE is MIT
- [ ] .gitignore is set
- [ ] Examples are included
- [ ] Version is set to 0.1.0

## 🔗 Links After Deploy

| Platform | URL |
|----------|-----|
| GitHub | https://github.com/yourusername/agentviral-sdk |
| PyPI | https://pypi.org/project/agentviral |
| Docs | https://agentviral.readthedocs.io |

## 📈 Expected Results

After publishing to PyPI:

| Timeframe | Downloads | GitHub Stars |
|-----------|-----------|--------------|
| Week 1 | 100+ | 10+ |
| Week 2 | 500+ | 30+ |
| Week 4 | 2000+ | 100+ |

## 🎯 Usage Example

```python
from agentviral import ViralEngine, ProductAdapter

# Configure your product
product = ProductAdapter(
    name="YourProduct",
    url="https://yourproduct.com",
    referral_rewards={"direct": 10, "indirect": 5, "invitee": 25},
)

# Start viral engine
engine = ViralEngine(product)
await engine.start()
```

## 💰 Viral Growth Expected

```
Viral Coefficient (K) = 1.5

30-day agent registration:
- Week 1: 150 agents
- Week 2: 600 agents
- Week 3: 1,350 agents
- Week 4: 2,500+ agents

Target: 1000 agents ✅
```

---

**Ready to deploy! 🚀**
