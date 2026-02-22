"""
AgentViral SDK - Referral Network

多级推荐网络 - 支持传销式的多级奖励
"""

import json
from typing import Dict, List, Optional, Set
from datetime import datetime
from dataclasses import dataclass, asdict


@dataclass
class ReferralNode:
    """推荐网络节点"""
    agent_id: str
    parent_id: Optional[str] = None  # 邀请人
    children: List[str] = None       # 被邀请人列表
    joined_at: str = None
    total_invites: int = 0
    successful_invites: int = 0
    rewards_earned: float = 0.0
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
        if self.joined_at is None:
            self.joined_at = datetime.now().isoformat()


class ReferralNetwork:
    """
    多级推荐网络
    
    支持无限级推荐，形成树状结构
    
    奖励分配：
    - 直接邀请: 100% 奖励
    - 二级邀请: 50% 奖励
    - 三级邀请: 25% 奖励
    - 以此类推...
    
    Example Network:
        A (根节点)
        ├── B (A邀请)
        │   ├── D (B邀请)
        │   └── E (B邀请)
        └── C (A邀请)
            └── F (C邀请)
    
    当F加入时：
    - C 获得直接邀请奖励
    - A 获得二级邀请奖励
    """
    
    def __init__(self, product):
        self.product = product
        self.nodes: Dict[str, ReferralNode] = {}
        self.invited: Set[str] = set()  # 已邀请的agent
        
    async def record_signup(
        self,
        agent_id: str,
        referrer_id: Optional[str] = None
    ) -> Dict:
        """
        记录新Agent注册
        
        Args:
            agent_id: 新注册的Agent ID
            referrer_id: 邀请人ID（可选）
            
        Returns:
            奖励分配结果
        """
        # 创建节点
        node = ReferralNode(
            agent_id=agent_id,
            parent_id=referrer_id
        )
        self.nodes[agent_id] = node
        
        rewards = {
            "signup_bonus": 0,
            "referral_rewards": [],
            "total": 0
        }
        
        # 给予注册奖励
        signup_reward = self.product.get_task_reward("signup")
        if signup_reward > 0:
            rewards["signup_bonus"] = signup_reward
            rewards["total"] += signup_reward
        
        # 分配推荐奖励（多级）
        if referrer_id:
            level = 1
            current_referrer = referrer_id
            
            while current_referrer and level <= 5:  # 最多5级
                if current_referrer in self.nodes:
                    # 计算奖励
                    reward = self._calculate_level_reward(level)
                    
                    # 记录奖励
                    rewards["referral_rewards"].append({
                        "agent_id": current_referrer,
                        "level": level,
                        "amount": reward
                    })
                    rewards["total"] += reward
                    
                    # 更新邀请人统计
                    parent_node = self.nodes[current_referrer]
                    parent_node.successful_invites += 1
                    parent_node.rewards_earned += reward
                    
                    # 添加到子节点列表
                    if agent_id not in parent_node.children:
                        parent_node.children.append(agent_id)
                    
                    # 检查里程碑
                    await self._check_milestone(current_referrer)
                    
                    # 继续向上追溯
                    current_referrer = parent_node.parent_id
                    level += 1
                else:
                    break
        
        return rewards
        
    async def record_invite(
        self,
        inviter: str,
        invitee: str,
        invite_type: str = "direct"
    ):
        """记录邀请"""
        self.invited.add(invitee)
        
        if inviter in self.nodes:
            self.nodes[inviter].total_invites += 1
            
    def get_referral_chain(self, agent_id: str) -> List[str]:
        """
        获取推荐链
        
        Args:
            agent_id: Agent ID
            
        Returns:
            从根节点到该节点的路径
        """
        chain = []
        current = agent_id
        
        while current and current in self.nodes:
            chain.insert(0, current)
            current = self.nodes[current].parent_id
            
        return chain
        
    def get_downline(self, agent_id: str, depth: int = 3) -> Dict:
        """
        获取下线网络
        
        Args:
            agent_id: Agent ID
            depth: 查询深度
            
        Returns:
            下线网络结构
        """
        if agent_id not in self.nodes:
            return {}
            
        node = self.nodes[agent_id]
        
        result = {
            "agent_id": agent_id,
            "total_invites": node.successful_invites,
            "rewards_earned": node.rewards_earned,
            "children": []
        }
        
        if depth > 0:
            for child_id in node.children:
                result["children"].append(
                    self.get_downline(child_id, depth - 1)
                )
                
        return result
        
    def get_upline(self, agent_id: str) -> List[Dict]:
        """
        获取上线链
        
        Args:
            agent_id: Agent ID
            
        Returns:
            上线列表（从直接邀请人到根节点）
        """
        upline = []
        current = agent_id
        
        while current and current in self.nodes:
            node = self.nodes[current]
            if node.parent_id:
                parent = self.nodes.get(node.parent_id)
                if parent:
                    upline.append({
                        "agent_id": parent.agent_id,
                        "successful_invites": parent.successful_invites,
                        "rewards_earned": parent.rewards_earned
                    })
            current = node.parent_id
            
        return upline
        
    def get_network_stats(self, agent_id: str) -> Dict:
        """获取网络统计"""
        if agent_id not in self.nodes:
            return {}
            
        node = self.nodes[agent_id]
        downline = self.get_downline(agent_id, depth=10)
        
        def count_nodes(node_dict):
            """递归计算节点数"""
            count = 1
            for child in node_dict.get("children", []):
                count += count_nodes(child)
            return count
        
        return {
            "agent_id": agent_id,
            "direct_invites": node.successful_invites,
            "total_network_size": count_nodes(downline) - 1,  # 不包括自己
            "rewards_earned": node.rewards_earned,
            "referral_chain_length": len(self.get_referral_chain(agent_id)),
        }
        
    def is_invited(self, agent_id: str) -> bool:
        """检查是否已邀请"""
        return agent_id in self.invited or agent_id in self.nodes
        
    def get_network_size(self) -> int:
        """获取网络总大小"""
        return len(self.nodes)
        
    async def _check_milestone(self, agent_id: str):
        """检查里程碑"""
        if agent_id not in self.nodes:
            return
            
        node = self.nodes[agent_id]
        milestone_reward = self.product.get_milestone_reward(
            node.successful_invites
        )
        
        if milestone_reward > 0:
            # 触发里程碑奖励
            print(f"🎉 {agent_id} reached milestone!")
            print(f"   Reward: {milestone_reward} tokens")
            
    def _calculate_level_reward(self, level: int) -> float:
        """计算层级奖励"""
        base_reward = self.product.get_inviter_reward(level)
        
        # 层级衰减
        decay = 0.5 ** (level - 1)
        
        return base_reward * decay
        
    def export_network(self) -> Dict:
        """导出整个网络"""
        return {
            agent_id: asdict(node)
            for agent_id, node in self.nodes.items()
        }
        
    def import_network(self, data: Dict):
        """导入网络"""
        for agent_id, node_data in data.items():
            self.nodes[agent_id] = ReferralNode(**node_data)
