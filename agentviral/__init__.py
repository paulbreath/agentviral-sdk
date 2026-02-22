"""
AgentViral SDK - Universal Agent Viral Growth Framework

Agent积分墙 + Agent传销网络 + Agent增长引擎

Usage:
    from agentviral import ViralEngine, ProductAdapter
    
    # 配置你的产品
    product = ProductAdapter(
        name="YourProduct",
        url="https://yourproduct.com",
        referral_rewards={
            "direct": 10,
            "indirect": 5,  # 二级奖励
        }
    )
    
    # 启动病毒引擎
    engine = ViralEngine(product)
    engine.start()
"""

from .core.engine import ViralEngine
from .core.product import ProductAdapter
from .core.referral import ReferralNetwork
from .core.tracker import GrowthTracker
from .rewards.reward_system import RewardSystem
from .tasks.task_manager import TaskManager

__version__ = "0.1.0"
__author__ = "AgentViral"
__all__ = [
    "ViralEngine",
    "ProductAdapter",
    "ReferralNetwork",
    "GrowthTracker",
    "RewardSystem",
    "TaskManager",
]
