"""
AgentViral SDK - Task Manager

任务管理器 - Agent积分墙系统

Agent可以通过完成任务获得奖励
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REWARDED = "rewarded"


@dataclass
class Task:
    """任务"""
    task_id: str
    task_type: str
    title: str
    description: str
    reward: float
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = None
    completed_at: Optional[str] = None
    requirements: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class TaskManager:
    """
    任务管理器
    
    Agent积分墙系统：
    1. 发布任务
    2. Agent接取任务
    3. 验证完成
    4. 发放奖励
    
    任务类型：
    - signup: 注册
    - invite: 邀请
    - review: 评价
    - share: 分享
    - purchase: 购买
    - custom: 自定义
    """
    
    def __init__(self, product):
        self.product = product
        self.tasks: Dict[str, Task] = {}
        self.agent_tasks: Dict[str, List[str]] = {}  # agent_id -> task_ids
        self.completed_tasks: Dict[str, List[str]] = {}  # agent_id -> completed
        
        # 初始化默认任务
        self._init_default_tasks()
        
    def _init_default_tasks(self):
        """初始化默认任务"""
        default_tasks = [
            {
                "task_id": "task_signup",
                "task_type": "signup",
                "title": "注册账号",
                "description": "注册成为新用户",
                "reward": self.product.get_task_reward("signup") or 10,
            },
            {
                "task_id": "task_first_invite",
                "task_type": "invite",
                "title": "首次邀请",
                "description": "成功邀请1位新用户",
                "reward": self.product.get_task_reward("first_invite") or 15,
                "requirements": {"min_invites": 1},
            },
            {
                "task_id": "task_5_invites",
                "task_type": "invite",
                "title": "邀请达人",
                "description": "成功邀请5位新用户",
                "reward": self.product.get_task_reward("5_invites") or 50,
                "requirements": {"min_invites": 5},
            },
            {
                "task_id": "task_review",
                "task_type": "review",
                "title": "撰写评价",
                "description": "撰写一条产品评价",
                "reward": self.product.get_task_reward("review") or 5,
            },
            {
                "task_id": "task_share",
                "task_type": "share",
                "title": "社交分享",
                "description": "分享到社交媒体",
                "reward": self.product.get_task_reward("share") or 3,
            },
        ]
        
        for task_data in default_tasks:
            task = Task(**task_data)
            self.tasks[task.task_id] = task
            
    def get_available_tasks(self, agent_id: str) -> List[Task]:
        """
        获取Agent可用的任务
        
        Args:
            agent_id: Agent ID
            
        Returns:
            可用任务列表
        """
        completed = self.completed_tasks.get(agent_id, [])
        
        available = []
        for task in self.tasks.values():
            if task.task_id not in completed:
                available.append(task)
        
        return available
        
    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务详情"""
        return self.tasks.get(task_id)
        
    def assign_task(self, agent_id: str, task_id: str) -> bool:
        """
        分配任务给Agent
        
        Args:
            agent_id: Agent ID
            task_id: 任务ID
            
        Returns:
            是否成功
        """
        if task_id not in self.tasks:
            return False
        
        if agent_id not in self.agent_tasks:
            self.agent_tasks[agent_id] = []
        
        if task_id not in self.agent_tasks[agent_id]:
            self.agent_tasks[agent_id].append(task_id)
        
        self.tasks[task_id].status = TaskStatus.IN_PROGRESS
        
        return True
        
    async def complete_task(
        self,
        agent_id: str,
        task_id: str,
        proof: Optional[Dict] = None
    ) -> Dict:
        """
        完成任务
        
        Args:
            agent_id: Agent ID
            task_id: 任务ID
            proof: 完成证明
            
        Returns:
            完成结果
        """
        task = self.tasks.get(task_id)
        
        if not task:
            return {"success": False, "error": "Task not found"}
        
        # 验证任务完成
        if not await self._verify_task_completion(agent_id, task, proof):
            return {"success": False, "error": "Verification failed"}
        
        # 更新状态
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now().isoformat()
        
        # 记录完成
        if agent_id not in self.completed_tasks:
            self.completed_tasks[agent_id] = []
        self.completed_tasks[agent_id].append(task_id)
        
        # 发放奖励
        from ..rewards.reward_system import RewardSystem
        reward_system = RewardSystem(self.product)
        
        reward = await reward_system.distribute_task_reward(
            agent_id, task.task_type
        )
        
        task.status = TaskStatus.REWARDED
        
        return {
            "success": True,
            "task_id": task_id,
            "reward": task.reward,
            "reward_record": reward
        }
        
    def create_custom_task(
        self,
        title: str,
        description: str,
        reward: float,
        requirements: Optional[Dict] = None
    ) -> Task:
        """
        创建自定义任务
        
        Args:
            title: 任务标题
            description: 任务描述
            reward: 奖励金额
            requirements: 任务要求
            
        Returns:
            创建的任务
        """
        task_id = f"custom_{datetime.now().timestamp()}"
        
        task = Task(
            task_id=task_id,
            task_type="custom",
            title=title,
            description=description,
            reward=reward,
            requirements=requirements or {}
        )
        
        self.tasks[task_id] = task
        
        return task
        
    def get_agent_progress(self, agent_id: str) -> Dict:
        """获取Agent的任务进度"""
        available = self.get_available_tasks(agent_id)
        completed = self.completed_tasks.get(agent_id, [])
        
        total_reward = sum(
            self.tasks[tid].reward for tid in completed if tid in self.tasks
        )
        
        return {
            "agent_id": agent_id,
            "available_tasks": len(available),
            "completed_tasks": len(completed),
            "total_reward_earned": total_reward,
            "completion_rate": len(completed) / len(self.tasks) if self.tasks else 0
        }
        
    async def _verify_task_completion(
        self,
        agent_id: str,
        task: Task,
        proof: Optional[Dict]
    ) -> bool:
        """验证任务完成"""
        # 根据任务类型进行验证
        if task.task_type == "signup":
            # 验证是否已注册
            return True  # 简化处理
        
        elif task.task_type == "invite":
            # 验证邀请数量
            min_invites = task.requirements.get("min_invites", 1)
            # 这里需要查询实际邀请数
            return True  # 简化处理
        
        elif task.task_type == "review":
            # 验证评价
            return proof is not None and "review_id" in proof
        
        elif task.task_type == "share":
            # 验证分享
            return proof is not None and "share_url" in proof
        
        return True  # 默认通过
