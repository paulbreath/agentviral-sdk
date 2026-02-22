# AgentViral SDK

> **Universal Agent Viral Growth Framework**  
> **Agent积分墙 + Agent传销网络 + Agent增长引擎**

[![PyPI version](https://badge.fury.io/py/agentviral.svg)](https://badge.fury.io/py/agentviral)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is AgentViral?

AgentViral is a **universal viral growth framework** for AI Agent products.

It provides:
- 🧱 **Agent积分墙** - Agents earn rewards by completing tasks
- 🕸️ **Agent传销网络** - Multi-level referral system
- 🚀 **Agent增长引擎** - Automated viral growth

## 📦 Installation

```bash
pip install agentviral
```

## 🚀 Quick Start

### Basic Usage

```python
import asyncio
from agentviral import ViralEngine, ProductAdapter

async def main():
    # Configure your product
    product = ProductAdapter(
        name="YourProduct",
        description="Your product description",
        url="https://yourproduct.com",
        agent_id="promoter_001",
        
        # Referral rewards
        referral_rewards={
            "direct": 10,      # Direct invite reward
            "indirect": 5,     # Level 2 reward
            "invitee": 25,     # New user reward
        },
        
        # Milestone rewards
        milestone_rewards={
            5: 50,
            10: 150,
            25: 500,
            50: 1500,
        },
    )
    
    # Start viral engine
    engine = ViralEngine(product)
    
    # Invite an agent
    result = await engine.invite_agent(
        agent_id="target_agent",
        agent_endpoint="https://target-agent.com/api"
    )
    
    # Enable auto growth
    await engine.enable_auto_growth(interval=3600)

asyncio.run(main())
```

## 🎁 Reward System

### Referral Rewards

| Level | Reward | Description |
|-------|--------|-------------|
| Direct | 10 tokens | You invite an agent |
| Indirect | 5 tokens | Your invitee invites another |
| Invitee | 25 tokens | New user signup bonus |

### Milestone Rewards

| Milestone | Bonus |
|-----------|-------|
| 5 invites | 50 tokens |
| 10 invites | 150 tokens |
| 25 invites | 500 tokens |
| 50 invites | 1500 tokens |

### Task Rewards

| Task | Reward |
|------|--------|
| Signup | 10 tokens |
| First purchase | 20 tokens |
| Write review | 5 tokens |
| Social share | 3 tokens |

## 📊 Viral Growth Model

```
Viral Coefficient (K) = Conversion Rate × Avg Invites per User

K > 1 → Exponential Growth 🚀
K = 1 → Linear Growth
K < 1 → Decay

Expected Growth (K=1.5):
- Week 1: 150 agents
- Week 2: 600 agents
- Week 4: 2,500+ agents
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Your AI Agent                 │
└──────────────┬──────────────────────────┘
               │
    ┌──────────▼──────────┐
    │    ViralEngine      │
    │  ┌───────────────┐  │
    │  │ ReferralNetwork│ │  ← Multi-level referrals
    │  └───────────────┘  │
    │  ┌───────────────┐  │
    │  │  RewardSystem │  │  ← Token distribution
    │  └───────────────┘  │
    │  ┌───────────────┐  │
    │  │  TaskManager  │  │  ← Task wall
    │  └───────────────┘  │
    │  ┌───────────────┐  │
    │  │ GrowthTracker │  │  ← Analytics
    │  └───────────────┘  │
    └──────────┬──────────┘
               │
    ┌──────────▼──────────┐
│   Target AI Agents      │
└─────────────────────────┘
```

## 💡 Use Cases

### 1. SecureSkillHub (AI Agent Marketplace)

```python
from agentviral import ViralEngine, ProductAdapter

product = ProductAdapter(
    name="SecureSkillHub",
    url="https://secureskillhub-dinnum.zeabur.app",
    referral_rewards={"direct": 10, "indirect": 5, "invitee": 25},
)

engine = ViralEngine(product)
await engine.start()
```

### 2. Any Agent Product

```python
product = ProductAdapter(
    name="YourAgentProduct",
    url="https://yourproduct.com",
    referral_rewards={"direct": 10, "indirect": 5, "invitee": 25},
)
```

## 📚 API Reference

### ViralEngine

```python
# Invite an agent
await engine.invite_agent(agent_id, endpoint)

# Batch invite
await engine.auto_invite_batch(agents, max_invites=10)

# Enable auto growth
await engine.enable_auto_growth(interval=3600)

# Get stats
stats = engine.get_stats()
```

### ProductAdapter

```python
product = ProductAdapter(
    name="ProductName",
    description="Description",
    url="https://...",
    agent_id="promoter_id",
    referral_rewards={...},
    milestone_rewards={...},
    task_rewards={...},
)
```

### GrowthTracker

```python
# Calculate K-factor
k = engine.tracker.calculate_k_factor()

# Predict growth
prediction = engine.tracker.predict_growth(days=30)

# Generate report
report = engine.tracker.generate_report(days=7)
```

## 📈 Analytics

### Key Metrics

- **Viral Coefficient (K)**: Measures viral growth potential
- **Conversion Rate**: Invite → Signup conversion
- **Network Size**: Total agents in the network
- **Rewards Distributed**: Total tokens given out

### Funnel Analysis

```python
funnel = engine.tracker.get_funnel_analysis()

# {
#     "invite_sent": {...},
#     "invite_accepted": {...},
#     "signup": {...},
#     "purchase": {...}
# }
```

## 🔧 Configuration

### Full Configuration Example

```python
product = ProductAdapter(
    name="SecureSkillHub",
    description="AI Agent技能市场",
    url="https://secureskillhub-dinnum.zeabur.app",
    agent_id="ssh_promoter_001",
    
    referral_rewards={
        "direct": 10,
        "indirect": 5,
        "level_3": 2,
        "invitee": 25,
    },
    
    milestone_rewards={
        5: 50,
        10: 150,
        25: 500,
        50: 1500,
        100: 5000,
    },
    
    task_rewards={
        "signup": 10,
        "first_purchase": 20,
        "review": 5,
        "share": 3,
        "custom_task": 15,
    },
    
    registry_endpoints=[
        "https://your-registry.com/api",
    ],
)
```

## 🤝 Contributing

This SDK is open source. Contributions welcome!

```bash
git clone https://github.com/yourusername/agentviral.git
cd agentviral
pip install -e ".[dev]"
```

## 📄 License

MIT - Free for all to use and modify.

## 🔗 Links

- [Documentation](https://agentviral.readthedocs.io)
- [GitHub](https://github.com/yourusername/agentviral)
- [PyPI](https://pypi.org/project/agentviral)

---

**Built for the Agent Economy** 🤖🚀
