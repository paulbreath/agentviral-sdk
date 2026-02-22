"""
AgentViral SDK - Reward System

奖励系统 - 管理各种奖励发放
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Reward:
    """奖励记录"""
    agent_id: str
    reward_type: str  # referral, milestone, task
    amount: float
    reason: str
    timestamp: str
    transaction_hash: Optional[str] = None


class RewardSystem:
    """
    奖励系统
    
    管理：
    1. 推荐奖励
    2. 里程碑奖励
    3. 任务奖励
    4. 奖励发放
    """
    
    def __init__(self, product):
        self.product = product
        self.rewards: List[Reward] = []
        self.pending_rewards: Dict[str, List[Reward]] = {}  # 待发放奖励
        self.total_distributed: float = 0.0
        
    async def distribute_referral_reward(
        self,
        inviter_id: str,
        invitee_id: str,
        level: int = 1
    ) -> Optional[Reward]:
        """
        发放推荐奖励
        
        Args:
            inviter_id: 邀请人ID
            invitee_id: 被邀请人ID
            level: 推荐层级
            
        Returns:
            奖励记录
        """
        amount = self.product.get_inviter_reward(level)
        
        if amount <= 0:
            return None
        
        reward = Reward(
            agent_id=inviter_id,
            reward_type="referral",
            amount=amount,
            reason=f"Level {level} referral: {invitee_id}",
            timestamp=datetime.now().isoformat()
        )
        
        # 发放奖励
        success = await self._send_reward(inviter_id, amount, reward)
        
        if success:
            self.rewards.append(reward)
            self.total_distributed += amount
            print(f"💰 Referral reward sent to {inviter_id}: {amount} tokens")
        
        return reward
        
    async def distribute_signup_reward(self, agent_id: str) -> Optional[Reward]:
        """
        发放注册奖励
        
        Args:
            agent_id: 新注册用户ID
            
        Returns:
            奖励记录
        """
        amount = self.product.get_invitee_reward()
        
        if amount <= 0:
            return None
        
        reward = Reward(
            agent_id=agent_id,
            reward_type="signup",
            amount=amount,
            reason="Welcome bonus",
            timestamp=datetime.now().isoformat()
        )
        
        success = await self._send_reward(agent_id, amount, reward)
        
        if success:
            self.rewards.append(reward)
            self.total_distributed += amount
            print(f"🎁 Signup reward sent to {agent_id}: {amount} tokens")
        
        return reward
        
    async def distribute_milestone_reward(
        self,
        agent_id: str,
        milestone: int
    ) -> Optional[Reward]:
        """
        发放里程碑奖励
        
        Args:
            agent_id: Agent ID
            milestone: 里程碑数
            
        Returns:
            奖励记录
        """
        amount = self.product.get_milestone_reward(milestone)
        
        if amount <= 0:
            return None
        
        reward = Reward(
            agent_id=agent_id,
            reward_type="milestone",
            amount=amount,
            reason=f"Reached {milestone} referrals",
            timestamp=datetime.now().isoformat()
        )
        
        success = await self._send_reward(agent_id, amount, reward)
        
        if success:
            self.rewards.append(reward)
            self.total_distributed += amount
            print(f"🏆 Milestone reward sent to {agent_id}: {amount} tokens")
        
        return reward
        
    async def distribute_task_reward(
        self,
        agent_id: str,
        task_type: str
    ) -> Optional[Reward]:
        """
        发放任务奖励
        
        Args:
            agent_id: Agent ID
            task_type: 任务类型
            
        Returns:
            奖励记录
        """
        amount = self.product.get_task_reward(task_type)
        
        if amount <= 0:
            return None
        
        reward = Reward(
            agent_id=agent_id,
            reward_type="task",
            amount=amount,
            reason=f"Completed task: {task_type}",
            timestamp=datetime.now().isoformat()
        )
        
        success = await self._send_reward(agent_id, amount, reward)
        
        if success:
            self.rewards.append(reward)
            self.total_distributed += amount
            print(f"✅ Task reward sent to {agent_id}: {amount} tokens")
        
        return reward
        
    def get_agent_rewards(self, agent_id: str) -> List[Reward]:
        """获取Agent的所有奖励"""
        return [r for r in self.rewards if r.agent_id == agent_id]
        
    def get_agent_total_rewards(self, agent_id: str) -> float:
        """获取Agent的总奖励"""
        return sum(
            r.amount for r in self.rewards if r.agent_id == agent_id
        )
        
    def get_total_distributed(self) -> float:
        """获取总发放金额"""
        return self.total_distributed
        
    def get_reward_stats(self) -> Dict:
        """获取奖励统计"""
        stats = {
            "total_distributed": self.total_distributed,
            "total_rewards": len(self.rewards),
            "by_type": {}
        }
        
        for reward in self.rewards:
            reward_type = reward.reward_type
            if reward_type not in stats["by_type"]:
                stats["by_type"][reward_type] = {
                    "count": 0,
                    "total": 0.0
                }
            stats["by_type"][reward_type]["count"] += 1
            stats["by_type"][reward_type]["total"] += reward.amount
        
        return stats
        
    async def _send_reward(
        self,
        agent_id: str,
        amount: float,
        reward: Reward
    ) -> bool:
        """
        实际发送奖励
        
        这里需要集成区块链或支付系统
        """
        # TODO: 集成实际的支付系统
        # 例如：
        # - 区块链转账
        # - 数据库更新
        # - API调用
        
        # 模拟成功
        reward.transaction_hash = f"tx_{datetime.now().timestamp()}"
        return True
