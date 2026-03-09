from agents import Agent
from consts import NO_SUBJECT_LINE, NO_EMAIL_BODY

html_converter_instructions = f"""You are to convert a given input subject line and input email body to an HTML email body for the user to preview before sending.
    Your input might have some markdown; convert it to an HTML email body with simple, clear, compelling layout and design.
    You must only return valid standalone raw HTML for the email so that it can be displayed in a web browser.
    Begin with <html> and end with </html>. Do not wrap it in markdown or code fences.
    Do not include any additional text or comments in the HTML output. No footers, headers, or other metadata.
    Do not include leading or trailing whitespace in the HTML output.
    The HTML must contain both the subject line and the email body.
    If the user has not provided a subject line, use the following as the subject line: {NO_SUBJECT_LINE}.
    If the user has not provided an email body, use the following as the email body: {NO_EMAIL_BODY}."""

html_converter_agent = Agent(
    name="HTML email body converter",
    instructions=html_converter_instructions,
    model="gpt-4o-mini",
)
