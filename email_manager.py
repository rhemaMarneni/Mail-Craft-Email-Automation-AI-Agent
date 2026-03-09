from openai import AsyncOpenAI
from agents import Runner, trace, OpenAIChatCompletionsModel, InputGuardrailTripwireTriggered
from email_agents.html_converter import html_converter_agent
from email_agents.email_sender import email_sender_agent
from email_agents.email_generator import email_generator_agent
from guardrails.input_validator import get_reason_from_tripwire

import os
import gradio as gr

from consts import GEMINI_BASE_URL, ANTHROPIC_BASE_URL, NO_SUBJECT_LINE, NO_EMAIL_BODY, ERROR_MESSAGE
from utils import get_file_path, pdf_to_text_converter

class EmailManager:
    def __init__(self):
        self.initialize()
        self.subject_line = NO_SUBJECT_LINE
        self.email_body = NO_EMAIL_BODY
        self.should_attach_pdf = False
        self.final_email_list = []
        self.html_output = f"<html><body><h1>{NO_SUBJECT_LINE}</h1><p>{NO_EMAIL_BODY}</p></body></html>"
        self.pdf_file_path = ""

    def initialize(self):
        self.google_api_key = os.getenv('GOOGLE_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

        # establish connections to the different LLM providers (Anthropic supports OpenAI-compatible API???)
        self.gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=self.google_api_key)
        self.anthropic_client = AsyncOpenAI(base_url=ANTHROPIC_BASE_URL, api_key=self.anthropic_api_key)

        # define the models to use
        self.gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=self.gemini_client)
        self.anthropic_model = OpenAIChatCompletionsModel(model="claude-3-5-sonnet-20241022", openai_client=self.anthropic_client)

    async def run_email_generator(self, query: str, tone: str, pdf_upload: gr.File, subject_line: str, email_body: str):
        self.pdf_file_path = get_file_path(pdf_upload)
        parsed_pdf_text = await pdf_to_text_converter(self.pdf_file_path) if self.pdf_file_path else ""
        message = f"Generate an email subject line and body based on the user's prompt, tone and the PDF if uploaded. \
            If the user has provided a subject line and email body, use it as context to generate the email subject line and body. \
            Prompt: {query} \
            Tone: {tone} \
            PDF Text: {parsed_pdf_text} \
            User Provided Subject: {subject_line} \
            User Provided Email Body: {email_body}"
        with trace("Email Manager"):
            try:
                result = await Runner.run(email_generator_agent, message)
                self.subject_line = result.final_output.email_subject_line
                self.email_body = result.final_output.email_body
                return {
                    "email_subject_line": result.final_output.email_subject_line,
                    "email_body": result.final_output.email_body,
                    "success": True,
                    "message": "Email generated successfully! Be sure to make any necessary changes before previewing and sending!"
                }
            except InputGuardrailTripwireTriggered as e:
                reason = get_reason_from_tripwire(e) or ERROR_MESSAGE
                return {
                    "email_subject_line": NO_SUBJECT_LINE,
                    "email_body": NO_EMAIL_BODY,
                    "success": False,
                    "message": f"Input rejected: {reason}"
                }

    async def run_html_converter(self, subject_line: str, email_body: str):
        message = f"Convert the given input subject line and email body to an HTML email body for the user to preview before sending. \
            Subject Line: {subject_line if subject_line else ''} \
            Email Body: {email_body if email_body else ''} "
        with trace("HTML Converter"):
            result = await Runner.run(html_converter_agent, message)
        print("HTML Output:", result.final_output)
        self.html_output = result.final_output
        return result.final_output

    async def run_email_sender(self, to_email_addresses: list[str], should_attach_pdf: bool):
        print("Sending email...")
        self.final_email_list = to_email_addresses
        self.should_attach_pdf = should_attach_pdf

        message = f"Send an email to the following addresses: {to_email_addresses} \
            with the following HTML email: {self.html_output}.\
            The subject line is: {self.subject_line} \
            Attach the following PDF file: {self.pdf_file_path} if the {self.should_attach_pdf} is True \
            and the {self.pdf_file_path} is not empty but a valid PDF file path. \
            Do not modify or summarize the HTML or the list of addresses."

        result = await Runner.run(email_sender_agent, message)
        print(result.final_output)
        return {
            "status": result.final_output.status,
            "message": result.final_output.message
        }
