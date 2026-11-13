from enum import Enum
from pydantic import BaseModel, Field


class TicketType(str, Enum):
    INCIDENT = "incident"
    REQUEST = "request"
    PROBLEM = "problem"
    CHANGE = "change"
    OTHER = "other"


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TechnicalContext(BaseModel):
    affected_system: str | None = Field(None, description="Назва продукту, сервісу або модуля")
    error_code: str | None = Field(None, description="Код або текст помилки, якщо вказано")
    steps_already_tried: list[str] = Field(default_factory=list, description="Кроки, які вже виконав користувач")


class SupportTicketExtracted(BaseModel):
    language: str = Field(..., description="ISO 639-1 код мови звернення (en, de, es, uk тощо)")
    ticket_type: TicketType
    priority: PriorityLevel
    department: str = Field(..., description="Цільовий відділ (Technical Support, Billing, Sales тощо)")
    summary: str = Field(..., description="Коротка суть тікета англійською мовою (1 речення)")
    technical_context: TechnicalContext
    requires_human_escalation: bool = Field(..., description="Чи потрібне термінове втручання інженера")