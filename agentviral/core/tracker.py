"""
AgentViral SDK - Growth Tracker

增长追踪器 - 监控病毒传播效果
"""

import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class GrowthMetrics:
    """增长指标"""
    timestamp: str
    total_agents: int
    new_agents: int
    invites_sent: int
    invites_accepted: int
    viral_coefficient: float
    conversion_rate: float
    

class GrowthTracker:
    """
    增长追踪器
    
    追踪和分析病毒传播的各项指标
    
    核心指标：
    1. 病毒系数 (K-factor)
    2. 转化率
    3. 增长速度
    4. 网络效应
    """
    
    def __init__(self, product):
        self.product = product
        self.metrics_history: List[GrowthMetrics] = []
        self.daily_stats: Dict[str, Dict] = {}
        
    def record_event(self, event_type: str, data: Dict):
        """
        记录事件
        
        Args:
            event_type: 事件类型 (invite_sent, invite_accepted, signup, etc.)
            data: 事件数据
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in self.daily_stats:
            self.daily_stats[today] = {
                "invites_sent": 0,
                "invites_accepted": 0,
                "signups": 0,
                "purchases": 0,
            }
        
        if event_type in self.daily_stats[today]:
            self.daily_stats[today][event_type] += 1
            
    def calculate_k_factor(self, days: int = 7) -> float:
        """
        计算病毒系数 (K-factor)
        
        K = 每个用户带来的新用户数
        
        K > 1: 病毒式增长
        K = 1: 稳定状态
        K < 1: 衰减
        
        Args:
            days: 计算时间窗口（天）
            
        Returns:
            病毒系数
        """
        # 获取最近N天的数据
        recent_stats = self._get_recent_stats(days)
        
        total_invites_sent = sum(
            s.get("invites_sent", 0) for s in recent_stats
        )
        total_invites_accepted = sum(
            s.get("invites_accepted", 0) for s in recent_stats
        )
        
        if total_invites_sent == 0:
            return 0.0
        
        # 转化率
        conversion_rate = total_invites_accepted / total_invites_sent
        
        # 平均每个用户发送的邀请数
        avg_invites_per_user = total_invites_sent / max(len(recent_stats), 1)
        
        # K = 转化率 × 平均邀请数
        k_factor = conversion_rate * avg_invites_per_user
        
        return round(k_factor, 2)
        
    def calculate_conversion_rate(
        self,
        from_step: str,
        to_step: str,
        days: int = 7
    ) -> float:
        """
        计算转化率
        
        Args:
            from_step: 起始步骤
            to_step: 目标步骤
            days: 时间窗口
            
        Returns:
            转化率 (0-1)
        """
        recent_stats = self._get_recent_stats(days)
        
        from_count = sum(s.get(from_step, 0) for s in recent_stats)
        to_count = sum(s.get(to_step, 0) for s in recent_stats)
        
        if from_count == 0:
            return 0.0
            
        return round(to_count / from_count, 4)
        
    def calculate_growth_rate(self, days: int = 7) -> float:
        """
        计算增长率
        
        Args:
            days: 时间窗口
            
        Returns:
            增长率 (例如: 0.15 = 15%)
        """
        recent_stats = self._get_recent_stats(days)
        
        if len(recent_stats) < 2:
            return 0.0
        
        # 计算每日增长
        daily_growth = []
        for i in range(1, len(recent_stats)):
            prev = recent_stats[i-1].get("signups", 0)
            curr = recent_stats[i].get("signups", 0)
            
            if prev > 0:
                growth = (curr - prev) / prev
                daily_growth.append(growth)
        
        if not daily_growth:
            return 0.0
            
        # 平均增长率
        avg_growth = sum(daily_growth) / len(daily_growth)
        
        return round(avg_growth, 4)
        
    def predict_growth(self, days: int = 30) -> Dict:
        """
        预测增长
        
        Args:
            days: 预测天数
            
        Returns:
            预测结果
        """
        k_factor = self.calculate_k_factor()
        current_users = self._get_current_user_count()
        
        if k_factor <= 0:
            return {
                "current_users": current_users,
                "predicted_users": current_users,
                "growth_type": "stable"
            }
        
        # 病毒增长公式
        # N(t) = N0 × K^t
        predicted_users = current_users * (k_factor ** days)
        
        growth_type = "viral" if k_factor > 1 else "linear" if k_factor == 1 else "decay"
        
        return {
            "current_users": current_users,
            "predicted_users": int(predicted_users),
            "k_factor": k_factor,
            "growth_type": growth_type,
            "days": days
        }
        
    def get_funnel_analysis(self) -> Dict:
        """
        获取漏斗分析
        
        Returns:
            漏斗数据
        """
        return {
            "invite_sent": {
                "count": self._get_total("invites_sent"),
                "conversion_to_accepted": self.calculate_conversion_rate(
                    "invites_sent", "invites_accepted"
                )
            },
            "invite_accepted": {
                "count": self._get_total("invites_accepted"),
                "conversion_to_signup": self.calculate_conversion_rate(
                    "invites_accepted", "signups"
                )
            },
            "signup": {
                "count": self._get_total("signups"),
                "conversion_to_purchase": self.calculate_conversion_rate(
                    "signups", "purchases"
                )
            },
            "purchase": {
                "count": self._get_total("purchases"),
            }
        }
        
    def get_daily_report(self, date: Optional[str] = None) -> Dict:
        """
        获取日报
        
        Args:
            date: 日期 (默认今天)
            
        Returns:
            日报数据
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        stats = self.daily_stats.get(date, {})
        
        return {
            "date": date,
            "invites_sent": stats.get("invites_sent", 0),
            "invites_accepted": stats.get("invites_accepted", 0),
            "signups": stats.get("signups", 0),
            "purchases": stats.get("purchases", 0),
            "conversion_rate": self.calculate_conversion_rate(
                "invites_sent", "signups"
            )
        }
        
    def generate_report(self, days: int = 7) -> Dict:
        """
        生成完整报告
        
        Args:
            days: 报告时间范围
            
        Returns:
            完整报告
        """
        return {
            "product": self.product.name,
            "period_days": days,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "k_factor": self.calculate_k_factor(days),
                "growth_rate": self.calculate_growth_rate(days),
                "total_users": self._get_current_user_count(),
            },
            "funnel": self.get_funnel_analysis(),
            "prediction": self.predict_growth(30),
            "daily_breakdown": [
                self.get_daily_report(
                    (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
                )
                for i in range(days)
            ]
        }
        
    def _get_recent_stats(self, days: int) -> List[Dict]:
        """获取最近N天的统计"""
        stats = []
        
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
            if date in self.daily_stats:
                stats.append(self.daily_stats[date])
                
        return stats
        
    def _get_total(self, metric: str) -> int:
        """获取总计"""
        return sum(s.get(metric, 0) for s in self.daily_stats.values())
        
    def _get_current_user_count(self) -> int:
        """获取当前用户数"""
        return self._get_total("signups")
