"""
AgentViral SDK - 通用产品使用示例

展示如何使用AgentViral SDK推广任何产品
"""

import asyncio
from agentviral import ViralEngine, ProductAdapter


async def main():
    """通用产品推广示例"""
    
    print("=== AgentViral SDK - Generic Product Demo ===\n")
    
    # 配置你的产品
    product = ProductAdapter(
        name="YourProduct",
        description="Your product description",
        url="https://yourproduct.com",
        agent_id="your_promoter_001",
        
        # 推荐奖励
        referral_rewards={
            "direct": 10,
            "indirect": 5,
            "invitee": 25,
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
    )
    
    # 启动病毒引擎
    engine = ViralEngine(product)
    
    # 启用自动增长模式
    # await engine.enable_auto_growth(interval=3600)
    
    # 或者手动邀请
    result = await engine.invite_agent(
        agent_id="target_agent_001",
        agent_endpoint="https://target-agent.com/api"
    )
    
    print(f"Invite result: {result}")
    
    # 获取统计
    stats = engine.get_stats()
    print(f"Stats: {stats}")


if __name__ == "__main__":
    asyncio.run(main())
