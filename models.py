from pydantic import BaseModel, Field
from typing import Literal

class CustomerAccountContext(BaseModel):
    customer_id: str
    name: str


class GuardrailDecision(BaseModel):
    decision: Literal["allow", "block"]
    reason: str
    explanation: str

    
class HandoffData(BaseModel):
    to_agent_name :str
    issue_type: str
    issue_description: str
    reason: str

class TriageOutputGuardRailOutput(BaseModel):
    contains_off_topic: bool
    contains_credential: bool
    reason: str