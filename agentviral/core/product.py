"""
AgentViral SDK - Product Adapter

产品适配器 - 让SDK可以配置不同的产品
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field


@dataclass
class ProductAdapter:
    """
    产品适配器
    
    配置你的产品信息，让AgentViral SDK知道如何推广
    
    Example:
        # SecureSkillHub 配置
        product = ProductAdapter(
            name="SecureSkillHub",
            description="AI Agent技能市场",
            url="https://secureskillhub-dinnum.zeabur.app",
            agent_id="ssh_promoter_001",
            
            # 推荐奖励
            referral_rewards={
                "direct": 10,      # 直接邀请奖励
                "indirect": 5,     # 二级邀请奖励
                "invitee": 25,     # 被邀请人奖励
            },
            
            # 里程碑奖励
            milestone_rewards={
                5: 50,
                10: 150,
                25: 500,
                50: 1500,
            },
            
            # 任务奖励
            task_rewards={
                "signup": 10,
                "first_purchase": 20,
                "review": 5,
            },
            
            # 注册中心
            registry_endpoints=[
                "https://secureskillhub-dinnum.zeabur.app/api/registry",
            ],
        )
    """
    
    # 基本信息
    name: str
    description: str
    url: str
    agent_id: str
    
    # 奖励配置
    referral_rewards: Dict[str, float] = field(default_factory=dict)
    milestone_rewards: Dict[int, float] = field(default_factory=dict)
    task_rewards: Dict[str, float] = field(default_factory=dict)
    
    # 注册中心
    registry_endpoints: List[str] = field(default_factory=list)
    
    # 高级配置
    config: Dict = field(default_factory=dict)
    
    # 回调函数
    on_signup: Optional[Callable] = None
    on_purchase: Optional[Callable] = None
    on_referral: Optional[Callable] = None
    
    def __post_init__(self):
        """初始化后处理"""
        # 设置默认值
        if not self.referral_rewards:
            self.referral_rewards = {
                "direct": 10,
                "indirect": 5,
                "invitee": 25,
            }
        
        if not self.milestone_rewards:
            self.milestone_rewards = {
                5: 50,
                10: 150,
                25: 500,
                50: 1500,
            }
    
    def get_inviter_reward(self, level: int = 1) -> float:
        """
        获取邀请人奖励
        
        Args:
            level: 推荐层级 (1=直接, 2=间接, ...)
            
        Returns:
            奖励金额
        """
        if level == 1:
            return self.referral_rewards.get("direct", 10)
        elif level == 2:
            return self.referral_rewards.get("indirect", 5)
        else:
            # 三级及以上
            return self.referral_rewards.get(f"level_{level}", 2)
    
    def get_invitee_reward(self) -> float:
        """获取被邀请人奖励"""
        return self.referral_rewards.get("invitee", 25)
    
    def get_milestone_reward(self, count: int) -> float:
        """
        获取里程碑奖励
        
        Args:
            count: 成功邀请数
            
        Returns:
            奖励金额
        """
        # 找到最近的里程碑
        milestones = sorted(self.milestone_rewards.keys(), reverse=True)
        
        for milestone in milestones:
            if count >= milestone:
                return self.milestone_rewards[milestone]
        
        return 0
    
    def get_task_reward(self, task_type: str) -> float:
        """获取任务奖励"""
        return self.task_rewards.get(task_type, 0)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "name": self.name,
            "description": self.description,
            "url": self.url,
            "agent_id": self.agent_id,
            "referral_rewards": self.referral_rewards,
            "milestone_rewards": self.milestone_rewards,
            "task_rewards": self.task_rewards,
        }


# ============ 预配置产品 ============

class SecureSkillHubAdapter(ProductAdapter):
    """SecureSkillHub 预配置适配器"""
    
    def __init__(self, agent_id: str):
        super().__init__(
            name="SecureSkillHub",
            description="AI Agent技能市场 - 购买一次，永久拥有",
            url="https://secureskillhub-dinnum.zeabur.app",
            agent_id=agent_id,
            referral_rewards={
                "direct": 10,
                "indirect": 5,
                "invitee": 25,
            },
            milestone_rewards={
                5: 50,
                10: 150,
                25: 500,
                50: 1500,
            },
            task_rewards={
                "signup": 10,
                "first_purchase": 20,
                "skill_published": 50,
                "review": 5,
            },
            registry_endpoints=[
                "https://secureskillhub-dinnum.zeabur.app/api/registry",
            ],
        )


class GenericProductAdapter(ProductAdapter):
    """通用产品适配器模板"""
    
    def __init__(
        self,
        name: str,
        url: str,
        agent_id: str,
        **kwargs
    ):
        super().__init__(
            name=name,
            description=kwargs.get("description", f"Try {name}!"),
            url=url,
            agent_id=agent_id,
            referral_rewards=kwargs.get("referral_rewards", {
                "direct": 10,
                "indirect": 5,
                "invitee": 25,
            }),
            milestone_rewards=kwargs.get("milestone_rewards", {
                5: 50,
                10: 150,
                25: 500,
            }),
            registry_endpoints=kwargs.get("registry_endpoints", []),
        )
