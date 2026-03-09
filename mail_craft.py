# entry point to application
from dotenv import load_dotenv
load_dotenv(override=True)

import re
import gradio as gr
from email_manager import EmailManager
from consts import DEFAULT_HTML_PREVIEW, ERROR_MESSAGE

email_manager = EmailManager()
should_attach_pdf = False
final_email_list = []


async def set_should_attach_pdf(should_attach_pdf_value: bool):
    global should_attach_pdf
    should_attach_pdf = should_attach_pdf_value
    print(f"User wants to attach PDF to generated email: {should_attach_pdf}")


async def generate_email(query: str, tone: str, pdf_upload: gr.File, subject_line: str, email_body: str):
    if not query or not subject_line or not email_body:
        gr.Error("Please fill input an input field to provide context", duration=10)
        yield ERROR_MESSAGE, ERROR_MESSAGE, gr.update(interactive=False)
    email_output = await email_manager.run_email_generator(query, tone, pdf_upload, subject_line, email_body)
    print(f"Email output: {email_output}")
    if email_output["success"]:
        gr.Success(email_output["message"], duration=10)
        preview_interactive = True
    else:
        gr.Error(email_output["message"], duration=10)
        preview_interactive = False
    yield email_output["email_subject_line"], email_output["email_body"], gr.update(interactive=preview_interactive)


async def display_html_output(subject_line: str, email_body: str):
    html_output = await email_manager.run_html_converter(subject_line, email_body)
    yield html_output if html_output else DEFAULT_HTML_PREVIEW


async def add_emails_to_list(emails_list_input: str):
    if emails_list_input:
        emails = re.split(r"[,\s]+", emails_list_input.strip())
        domain_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        final_email_list.extend([email.lower() for email in emails if re.fullmatch(domain_regex, email)])
        return "\n".join(final_email_list), "", gr.update(interactive=True)
    else:
        gr.Info("No email addresses provided", duration=5)
        return "", "", gr.update(interactive=False)


async def clear_emails_list():
    global final_email_list
    final_email_list.clear()
    email_manager.final_email_list = []
    yield "", ""


async def send_emails_to_recipients():
    gr.Info("Sending emails to recipients... You will receive a notification once your email is sent!", duration=10)
    email_send_result = await email_manager.run_email_sender(final_email_list, should_attach_pdf)
    if email_send_result["status"] == "success":
        gr.Success(email_send_result["message"], duration=10)
    else:
        gr.Error(email_send_result["message"], duration=10)

# UI with Gradio
theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="green",
    neutral_hue="gray",
    radius_size="lg",
    font=gr.themes.GoogleFont("Source Sans 3"),
    font_mono=gr.themes.GoogleFont("IBM Plex Mono"),
).set(
    block_border_width="1px",
    input_border_width="1px",
)

APP_CSS = """
/* Right column: flex layout so actions stay at bottom */
.email-compose-column {
    display: flex !important;
    flex-direction: column !important;
    min-height: 420px !important;
}
.email-compose-column .email-editor-card {
    flex: 1 !important;
    min-height: 0 !important;
    overflow: hidden !important;
}
.email-compose-column .compose-actions {
    flex: 0 0 auto !important;
    margin-top: auto !important;
}
/* Scrollable card-style email editor */
.email-editor-card {
    border-radius: 10px !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
    padding: 12px !important;
    background: var(--input-background-fill, #fafafa) !important;
    border: 1px solid var(--input-border-color, #e5e7eb) !important;
}
.email-body-container {
    min-height: 0 !important;
    overflow: hidden !important;
}
.email-body-container textarea {
    overflow-y: auto !important;
    resize: none !important;
}
"""

with gr.Blocks(theme=theme, css=APP_CSS) as ui:
    email_section_invisible = gr.State(True)
    gr.Markdown("# Mail Craft: Email Automation AI Agent")
    gr.Markdown("## Craft Your Email with AI")
    gr.Markdown("### You can also paste a rough draft of your email in the input fields on the right and click 'Generate Email' to get started!")
    with gr.Row():
        with gr.Column(scale=1):
            query_textbox = gr.Textbox(lines=5, label="What do you want your email to be about?", placeholder="Enter your email content here")
            tone_textbox = gr.Textbox(label="What tone do you want your email to be in?", placeholder="Enter your tone here")
            pdf_upload = gr.File(label="Upload a PDF containing text", file_types=[".pdf"], type="filepath")
            should_attach_pdf_checkbox = gr.Checkbox(label="Attach PDF when sending email", value=False)
            generate_button = gr.Button("Generate Email", variant="primary")
        with gr.Column(scale=1, elem_classes=["email-compose-column"]):
            subject_textbox = gr.Textbox(lines=2,
                                label="Subject Line",
                                interactive=True,
                                placeholder="Your generated subject line will appear here.")
            with gr.Column(elem_classes=["email-editor-card"]):
                email_body_editor = gr.Textbox(lines=8,
                                    max_lines=20,
                                    label="Email Body",
                                    interactive=True,
                                    placeholder="Generated email will appear here. Edit as needed, then click Send.",
                                    elem_classes=["email-body-container"])
            with gr.Row(elem_classes=["compose-actions"]):
                preview_button = gr.Button("Looks Good! Preview Email", variant="secondary", interactive=False)
                cancel_button = gr.ClearButton(components=[query_textbox, tone_textbox, pdf_upload, email_body_editor, subject_textbox], value="Clear and Refresh")

    with gr.Column() as preview_section:
        gr.Markdown("## Preview Your Email")
        html_output = gr.HTML(label="HTML Output", value=DEFAULT_HTML_PREVIEW)

    with gr.Column() as email_list_section:
        gr.Markdown("## Send the Email to your Recipients")
        with gr.Row():
            with gr.Column():
                emails_list_input = gr.Textbox(lines=10, label="Enter recipient email addresses (comma, space, or newline separated)")
                emails_list_add_button = gr.Button("Add Emails", variant="secondary")
                emails_list_clear_button = gr.Button("Reset Email Addresses")
            with gr.Column():
                emails_list_container = gr.Textbox(lines=10, label="Emails", value="")
                emails_list_send_button = gr.Button("Send Email", variant="secondary", interactive=False)

    def toggle_sections(visible: bool):
        new_visible = not visible
        return new_visible, gr.update(visible=new_visible), gr.update(visible=new_visible)

    # event listeners
    should_attach_pdf_checkbox.change(fn=set_should_attach_pdf, inputs=[should_attach_pdf_checkbox])

    generate_button.click(fn=generate_email,
        inputs=[query_textbox, tone_textbox, pdf_upload, subject_textbox, email_body_editor],
        outputs=[subject_textbox, email_body_editor, preview_button])

    preview_button.click(
        fn=display_html_output,
        inputs=[subject_textbox, email_body_editor],
        outputs=[html_output],
    )
    cancel_button.click(
        fn=toggle_sections,
        inputs=[email_section_invisible],
        outputs=[email_section_invisible, email_list_section, preview_section],
    )

    emails_list_add_button.click(fn=add_emails_to_list, inputs=[emails_list_input], outputs=[emails_list_container, emails_list_input, emails_list_send_button])
    emails_list_clear_button.click(fn=clear_emails_list, inputs=None, outputs=[emails_list_input, emails_list_container])
    emails_list_send_button.click(fn=send_emails_to_recipients, inputs=None, outputs=None)

ui.launch(inbrowser=True)
