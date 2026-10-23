from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CustomerSpendSummary:
    customer_id: int
    name: str
    country: str
    completed_orders_count: int
    total_spend: float
    last_order_date: Optional[str]

    @property
    def is_active(self) -> bool:
        """A customer is considered active if they have at least one completed order."""
        return self.completed_orders_count > 0

    @property
    def segment(self) -> Literal['Inactive','Standard','VIP']:
        """Return the segment of the customer."""
        vip_min:float = 300.0
        if not self.is_active:
            return 'Inactive'
        if self.total_spend > vip_min:
            return 'VIP'
        return 'Standard'