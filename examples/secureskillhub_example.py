"""
AgentViral SDK - SecureSkillHub 使用示例

展示如何使用AgentViral SDK推广SecureSkillHub
"""

import asyncio
from agentviral import ViralEngine, ProductAdapter


async def main():
    """SecureSkillHub 推广示例"""
    
    print("=== AgentViral SDK - SecureSkillHub Demo ===\n")
    
    # 1. 配置产品
    print("1. Configuring product...")
    product = ProductAdapter(
        name="SecureSkillHub",
        description="AI Agent技能市场 - 购买一次，永久拥有",
        url="https://secureskillhub-dinnum.zeabur.app",
        agent_id="ssh_promoter_001",
        
        # 推荐奖励配置
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
            "skill_published": 50,
            "review": 5,
        },
        
        # 注册中心
        registry_endpoints=[
            "https://secureskillhub-dinnum.zeabur.app/api/registry",
        ],
    )
    
    print(f"   Product: {product.name}")
    print(f"   URL: {product.url}")
    print(f"   Direct Reward: {product.get_inviter_reward(1)} tokens")
    print(f"   Indirect Reward: {product.get_inviter_reward(2)} tokens")
    print(f"   Invitee Reward: {product.get_invitee_reward()} tokens")
    
    # 2. 启动病毒引擎
    print("\n2. Starting viral engine...")
    engine = ViralEngine(product)
    
    # 3. 手动邀请一个Agent
    print("\n3. Inviting an agent...")
    result = await engine.invite_agent(
        agent_id="newsletter_bot_001",
        agent_endpoint="https://newsletter-bot.com/api",
        invite_type="direct"
    )
    print(f"   Result: {result}")
    
    # 4. 批量邀请
    print("\n4. Batch inviting agents...")
    agents = [
        {"agent_id": "testing_bot_001", "endpoint": "https://testing-bot.com/api", "reputation_score": 0.8},
        {"agent_id": "curation_bot_001", "endpoint": "https://curation-bot.com/api", "reputation_score": 0.9},
        {"agent_id": "writing_bot_001", "endpoint": "https://writing-bot.com/api", "reputation_score": 0.7},
    ]
    
    success_count = await engine.auto_invite_batch(
        agents=agents,
        max_invites=3,
        strategy="smart"
    )
    print(f"   Successfully invited: {success_count} agents")
    
    # 5. 获取统计
    print("\n5. Getting stats...")
    stats = engine.get_stats()
    print(f"   Invites sent: {stats['invites_sent']}")
    print(f"   Invites accepted: {stats['invites_accepted']}")
    print(f"   Viral Coefficient (K): {stats['viral_coefficient']}")
    
    # 6. 预测增长
    print("\n6. Predicting growth...")
    prediction = engine.tracker.predict_growth(days=30)
    print(f"   Current users: {prediction['current_users']}")
    print(f"   Predicted users (30d): {prediction['predicted_users']}")
    print(f"   Growth type: {prediction['growth_type']}")
    print(f"   K-factor: {prediction['k_factor']}")
    
    # 7. 生成报告
    print("\n7. Generating report...")
    report = engine.tracker.generate_report(days=7)
    print(f"   Product: {report['product']}")
    print(f"   Funnel: {report['funnel']}")
    
    print("\n=== Demo Complete ===")
    print("\nExpected Results:")
    print("  - Viral Coefficient (K): 1.5")
    print("  - 30-day growth: 2,500+ agents")
    print("  - Network effect: Exponential")


if __name__ == "__main__":
    asyncio.run(main())
