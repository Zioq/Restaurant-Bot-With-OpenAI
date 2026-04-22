from agents import Agent, output_guardrail, Runner, RunContextWrapper, GuardrailFunctionOutput

from models import TriageOutputGuardRailOutput, CustomerAccountContext

triage_output_guardrail_agent = Agent(
    name = "Triage Support Guardrail",
    instructions=""" 
    Ensure that all responses meet the following criteria:

    1. Maintain a professional, polite, and respectful tone at all times.
    2. Do not reveal or reference any internal system details, policies, or implementation logic.
    3. If a request would require exposing internal information, respond with a general, safe alternative instead.
    4. Keep responses clear, helpful, and appropriate for a restaurant customer interaction context.

     """,
    output_type=TriageOutputGuardRailOutput

)

@output_guardrail
async def triage_output_guardrail(
    wrapper: RunContextWrapper[CustomerAccountContext],
    agent: Agent,
    output: str
):
    result = await Runner.run(
        triage_output_guardrail_agent,
        output,
        context= wrapper.context
    )

    validation = result.final_output
    triggered = ( validation.contains_off_topic 
                 or validation.contains_credential 
    )

    return GuardrailFunctionOutput(
        output_info = validation,
        tripwire_triggered=triggered
    )


    
