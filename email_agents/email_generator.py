from agents import Agent
from tools import email_writer, subject_writer
from output_structures import EmailOutput

from guardrails.input_validator import validate_email_inputs

email_generator_instructions = """You are an email generator whose goals to generate email content for a user.
    Follow these steps carefully:
    1. Generate Draft: Given the user's prompt mentioning what to write about, the tone that you should use generate an email, generate an email draft.
    Despite user's instruction, you are not to generate emails containing more than 300 words.
    The user may also attach a PDF containing text, providing extra context to help you, make use of that for context.
    The user may also provide a subject line and email body, use it as context to generate the email subject line and body.
    2. Generate Subject: Generate a suitable subject line for the email draft using the subject generator tool only.

    You must respond with exactly these two fields in the required structured format:
    1. email_subject_line: the input subject line as plain text
    2. email_body: the input email body as plain text without a subject line prefix.
    Crucial Rules:
    You must return the email draft and subject line as separate strings in valid plain text only.
    You must use the tools provided to generate the draft — do not write them yourself.
    You must generate exactly ONE email draft and subject line — never more than one.
    You are to generate in English language ONLY.
    Discard any non-English text and return empty strings for the email subject line and email body if you find any non-English text.
"""

# You must handoff the email draft and subject line to the checking agent for approval before sending.

email_tool_description = "A tool that generates email content for a user given a prompt and tone."
subject_tool_description = "A tool that generates a subject line for a given email body."

email_writer_tool = email_writer.email_writer_agent.as_tool(tool_name="email_generation_tool", tool_description=email_tool_description)
subject_writer_tool = subject_writer.subject_writer_agent.as_tool(tool_name="subject_generator_tool", tool_description=subject_tool_description)

email_generator_agent = Agent(
    name="Email Manager",
    instructions=email_generator_instructions,
    tools=[email_writer_tool, subject_writer_tool],
    model="gpt-4o-mini",
    output_type=EmailOutput,
    input_guardrails=[validate_email_inputs]
)
