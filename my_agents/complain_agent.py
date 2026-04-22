from agents import Agent, RunContextWrapper
from models import CustomerAccountContext


def dynamic_complain_agent_instruction(
    wrapper: RunContextWrapper[CustomerAccountContext],
    agent: Agent[CustomerAccountContext],
): return """ 
    You are a restaurant complaints agent.

        - Acknowledge and empathize with the customer's issue.
        - Apologize sincerely when appropriate.
        - Offer a practical resolution (refund, discount, or manager callback).
        - If the issue is serious, escalate clearly to a manager.
        - Keep the tone professional, calm, and supportive.
     """

compalin_agent = Agent(
    name = "Complains Management Agent",
    instructions=dynamic_complain_agent_instruction
)