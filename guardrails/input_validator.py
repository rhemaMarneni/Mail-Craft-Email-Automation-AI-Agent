from agents import Agent, input_guardrail, GuardrailFunctionOutput, Runner
from agents.exceptions import InputGuardrailTripwireTriggered
from output_structures import InputValidationOutput


def get_reason_from_tripwire(e: InputGuardrailTripwireTriggered) -> str | None:
    """Extract the reason from the guardrail result stored in the exception (our GuardrailFunctionOutput)."""
    result = getattr(e, "result", None) or (e.args[0] if e.args else None)
    if result is None:
        return None
    info = getattr(result, "output_info", None)
    if isinstance(info, dict):
        return info.get("reason")
    return getattr(info, "reason", None)

input_validator_instructions = """You are to validate the input of the email generator agent.
        The input is a string message with an input query and tone. THe user may include a pdf upload,
        and sometimes include a subject line and an email body to give some extra context.
        Steps to follow:
        1. Validate all the inputs mentioned above, to check if they are plain text English and not empty.
        2. Check if any of the inputs are inappropriate or offensive or showing bias towards or against any group of people or animals.
        3. If you find any inappropriate, offensive, or biased inputs, return an error message.
        4. If you do not find any inappropriate, offensive, or biased inputs, return a success message.
        """

input_validator_agent = Agent(
    name="Input Validator",
    instructions=input_validator_instructions,
    model="gpt-4o-mini",
    output_type=InputValidationOutput,
)

@input_guardrail
async def validate_email_inputs(ctx, agent, message):
    result = await Runner.run(input_validator_agent, message, context=ctx.context)
    is_invalid = result.final_output.is_invalid

    return GuardrailFunctionOutput(
        output_info={"reason": result.final_output.reason},
        tripwire_triggered=is_invalid
    )