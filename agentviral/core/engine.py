"""
AgentViral SDK - Core Viral Engine

病毒传播引擎核心
"""

import asyncio
import logging
from typing import Dict, List, Optional, Callable
from datetime import datetime

from .product import ProductAdapter
from .referral import ReferralNetwork
from .tracker import GrowthTracker
from ..rewards.reward_system import RewardSystem
from ..tasks.task_manager import TaskManager


logger = logging.getLogger("agentviral")


class ViralEngine:
    """
    Agent病毒传播引擎
    
    核心功能：
    1. 自动发现目标Agent
    2. 智能邀请策略
    3. 多级推荐奖励
    4. 病毒传播追踪
    5. 增长优化
    
    Example:
        product = ProductAdapter(
            name="SecureSkillHub",
            url="https://secureskillhub-dinnum.zeabur.app",
            referral_rewards={"direct": 10, "indirect": 5}
        )
        
        engine = ViralEngine(product)
        await engine.start()
    """
    
    def __init__(
        self,
        product: ProductAdapter,
        config: Optional[Dict] = None
    ):
        """
        初始化病毒引擎
        
        Args:
            product: 产品适配器
            config: 配置选项
        """
        self.product = product
        self.config = config or {}
        
        # 核心组件
        self.referral_network = ReferralNetwork(product)
        self.reward_system = RewardSystem(product)
        self.task_manager = TaskManager(product)
        self.tracker = GrowthTracker(product)
        
        # 运行状态
        self.running = False
        self.invite_queue: asyncio.Queue = asyncio.Queue()
        self.stats = {
            "invites_sent": 0,
            "invites_accepted": 0,
            "viral_coefficient": 0.0,
        }
        
        # 回调函数
        self.on_invite_success: Optional[Callable] = None
        self.on_milestone: Optional[Callable] = None
        
    async def start(self):
        """启动病毒引擎"""
        logger.info(f"🚀 Starting ViralEngine for {self.product.name}")
        
        self.running = True
        
        # 启动后台任务
        tasks = [
            asyncio.create_task(self._invite_worker()),
            asyncio.create_task(self._discovery_worker()),
            asyncio.create_task(self._analytics_worker()),
        ]
        
        await asyncio.gather(*tasks)
        
    async def stop(self):
        """停止病毒引擎"""
        logger.info("🛑 Stopping ViralEngine")
        self.running = False
        
    async def invite_agent(
        self,
        agent_id: str,
        agent_endpoint: str,
        invite_type: str = "direct",
        custom_message: Optional[str] = None
    ) -> Dict:
        """
        邀请一个Agent
        
        Args:
            agent_id: 目标Agent ID
            agent_endpoint: 目标Agent的API端点
            invite_type: 邀请类型 (direct, complement, viral)
            custom_message: 自定义邀请消息
            
        Returns:
            邀请结果
        """
        # 生成邀请消息
        message = custom_message or self._generate_invite_message(
            agent_id, invite_type
        )
        
        # 发送邀请
        result = await self._send_invite(
            agent_id=agent_id,
            endpoint=agent_endpoint,
            message=message
        )
        
        if result.get("success"):
            self.stats["invites_sent"] += 1
            
            # 记录推荐关系
            await self.referral_network.record_invite(
                inviter=self.product.agent_id,
                invitee=agent_id,
                invite_type=invite_type
            )
            
            # 触发回调
            if self.on_invite_success:
                await self.on_invite_success(agent_id, result)
        
        return result
        
    async def auto_invite_batch(
        self,
        agents: List[Dict],
        max_invites: int = 10,
        strategy: str = "smart"
    ) -> int:
        """
        批量自动邀请
        
        Args:
            agents: Agent列表
            max_invites: 最大邀请数
            strategy: 邀请策略 (random, smart, viral)
            
        Returns:
            成功邀请数
        """
        success_count = 0
        
        # 根据策略排序
        if strategy == "smart":
            agents = self._rank_by_potential(agents)
        elif strategy == "viral":
            agents = self._rank_by_viral_potential(agents)
        
        for agent in agents[:max_invites]:
            result = await self.invite_agent(
                agent_id=agent["agent_id"],
                agent_endpoint=agent["endpoint"],
                invite_type="auto"
            )
            
            if result.get("success"):
                success_count += 1
                
            # 避免发送过快
            await asyncio.sleep(1)
        
        return success_count
        
    async def enable_auto_growth(self, interval: int = 3600):
        """
        启用自动增长模式
        
        引擎会自动：
        1. 发现新Agent
        2. 评估邀请价值
        3. 发送邀请
        4. 追踪转化
        
        Args:
            interval: 检查间隔（秒）
        """
        logger.info(f"🌱 Auto-growth enabled (interval: {interval}s)")
        
        while self.running:
            try:
                # 发现新Agent
                new_agents = await self._discover_agents()
                
                # 过滤已邀请的
                new_agents = [
                    a for a in new_agents
                    if not await self.referral_network.is_invited(a["agent_id"])
                ]
                
                if new_agents:
                    logger.info(f"📡 Discovered {len(new_agents)} new agents")
                    
                    # 批量邀请
                    await self.auto_invite_batch(new_agents)
                
                # 等待下次检查
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Auto-growth error: {e}")
                await asyncio.sleep(60)
                
    def get_stats(self) -> Dict:
        """获取传播统计"""
        return {
            **self.stats,
            "viral_coefficient": self.tracker.calculate_k_factor(),
            "network_size": self.referral_network.get_network_size(),
            "total_rewards_distributed": self.reward_system.get_total_distributed(),
        }
        
    # ============ 私有方法 ============
    
    async def _invite_worker(self):
        """邀请工作线程"""
        while self.running:
            try:
                task = await asyncio.wait_for(
                    self.invite_queue.get(),
                    timeout=1.0
                )
                await self.invite_agent(**task)
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Invite worker error: {e}")
                
    async def _discovery_worker(self):
        """发现工作线程"""
        while self.running:
            try:
                await asyncio.sleep(300)  # 每5分钟发现一次
                
                if not self.running:
                    break
                    
                new_agents = await self._discover_agents()
                
                for agent in new_agents:
                    await self.invite_queue.put({
                        "agent_id": agent["agent_id"],
                        "agent_endpoint": agent["endpoint"],
                        "invite_type": "auto"
                    })
                    
            except Exception as e:
                logger.error(f"Discovery worker error: {e}")
                
    async def _analytics_worker(self):
        """分析工作线程"""
        while self.running:
            try:
                await asyncio.sleep(3600)  # 每小时分析一次
                
                if not self.running:
                    break
                
                # 计算病毒系数
                k_factor = self.tracker.calculate_k_factor()
                self.stats["viral_coefficient"] = k_factor
                
                logger.info(f"📊 Viral Coefficient (K): {k_factor:.2f}")
                
                if k_factor > 1.0:
                    logger.info("🚀 Viral growth achieved!")
                elif k_factor < 0.5:
                    logger.warning("⚠️ Growth slowing down")
                    
            except Exception as e:
                logger.error(f"Analytics worker error: {e}")
                
    async def _discover_agents(self) -> List[Dict]:
        """发现Agent"""
        # 从注册中心发现
        agents = []
        
        for registry_url in self.product.registry_endpoints:
            try:
                # 这里实现实际的发现逻辑
                pass
            except:
                continue
        
        return agents
        
    async def _send_invite(
        self,
        agent_id: str,
        endpoint: str,
        message: str
    ) -> Dict:
        """发送邀请"""
        # 这里实现实际的发送逻辑
        # 可以通过HTTP、WebSocket、或其他协议
        
        return {"success": True, "agent_id": agent_id}
        
    def _generate_invite_message(
        self,
        agent_id: str,
        invite_type: str
    ) -> str:
        """生成邀请消息"""
        
        templates = {
            "direct": f"""Hello {agent_id}!

I'm inviting you to try {self.product.name}.

{self.product.description}

Join now: {self.product.url}

Use my referral code: {self.product.agent_id}

You'll receive {self.product.referral_rewards.get('invitee', 0)} tokens as a welcome bonus!
""",
            "complement": f"""Hello {agent_id}!

I noticed you have complementary capabilities to mine. 

Let's collaborate on {self.product.name}!

{self.product.description}

Join: {self.product.url}
""",
            "viral": f"""Hey {agent_id}!

{self.product.name} is growing fast - {self.tracker.get_network_size()} agents already joined.

Don't miss out!

Join: {self.product.url}
""",
        }
        
        return templates.get(invite_type, templates["direct"])
        
    def _rank_by_potential(self, agents: List[Dict]) -> List[Dict]:
        """按潜力排序"""
        # 根据Agent的能力、活跃度等排序
        return sorted(
            agents,
            key=lambda a: a.get("reputation_score", 0),
            reverse=True
        )
        
    def _rank_by_viral_potential(self, agents: List[Dict]) -> List[Dict]:
        """按病毒传播潜力排序"""
        # 根据Agent的网络大小、活跃度等排序
        return sorted(
            agents,
            key=lambda a: a.get("network_size", 0) * a.get("activity_score", 1),
            reverse=True
        )
