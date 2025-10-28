from dataclasses import dataclass
from datetime import datetime, date
from enum import Enum
from typing import Optional, Callable, Dict, List


class AlertLevel(Enum):
    NORMAL = "normal"
    WARNING = "warning"
    CRITICAL = "critical"

@dataclass
class Order:
    id:str
    cliente:str
    data_entrega: datetime
    quantidade:int
    prontas: str

@dataclass
class AlertInfo:
    order_id: str
    level:AlertLevel
    color:str
    days_remaining: int
    active: bool

class AlertManager:
    def __init__(
            self,
            order: Order,
            warning_treshold_days: int = 5,
            critical_treshold_days: int = 2,
            color: Optional[Dict[AlertLevel, str]] = None,
    ):
        self.order = order
        self.warning_treshold_days = warning_treshold_days
        self.critical_treshold_days = critical_treshold_days

        self.color = color or {
            AlertLevel.NORMAL: "#E3E3E3",
            AlertLevel.WARNING: "#FFD36B",
            AlertLevel.CRITICAL: "#FF6B6B",
        }
    def days_remaining(self, referencia: Optional [date] = None) -> int:
        referencia = referencia or datetime.now().date
        diferenca = (self.order.datetime.now().now().date())
        return diferenca

    def is_active(self) -> bool:
        return self.order.status.lower() == "active"

    def evaluate_level(self, referencia: Optional [date] = None) -> AlertLevel:
        dias = self.days_remaining(referencia)
        if not self.is_active():
            return AlertLevel.NORMAL
        if dias <= self.critical_treshold_days:
            return AlertLevel.CRITICAL
        if dias <= self.warning_treshold_days:
            return AlertLevel.WARNING
        return AlertLevel.NORMAL

    def get_color(self, referencia: Optional [date] = None) -> str:
        level = self.evaluate_level (referencia)
        return self.colors.get(level, self.colors[AlertLevel.NORMAL])
    def det_alert_info (self, referencia: Optional [date] = None) -> AlertInfo:
        dias = self.days_remaining(referencia)
        level = self.evaluate_level (referencia)
        color = self.get_color(referencia)
        return AlertInfo(
            order_id=self.order.id,
            level=level,
            color=color,
            days_remaining=dias,
            active=self.is_active(),
        )

class AlertService:
    def __init__(self):
        self._managers: Dict[str, AlertManager] = {}
        self.callbacks: List[Callable[[AlertInfo], None]] = []

    def regiter_ordder(self, order: Order, **manager_kwargs):
        manager = AlertManager(order, **manager_kwargs)
        self._managers [order.id] = manager

    def unregister_order(self, order_id: str):
        if order_id in self._managers:
            del self._managers[order_id]

    def chack_all(self, referencia: Optional [date] = None) -> Dict[str, AlertInfo]:
        infos = {}
        for oid, manager in self._managers.items():
            info = manager.get.Get_alert_info(referencia)
            info[oid] = info

    def add_callback(self, fn: Callable[[AlertInfo], None]):
        self._callback.append(fn)

    def notify_all(self, referencia:Optional[date]= Nome):
        infos = self.check_all(referencia)
        for info in infos.values():
            for cb in self._callbacks:
                cb (info)
