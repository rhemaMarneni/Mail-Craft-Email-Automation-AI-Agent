# MailCraft AI: Email Automation System
MailCraft AI is a multi-agent workflow that generates, formats, and sends emails using LLM-powered agents with guardrails and automated delivery.

## Pitch
Do you want to send meeting minutes to your attendees/colleagues without the hassle of constructing end-to-end sentences and structuring? Or probably a sales pitch to possible customers? Or email hiring managers to hire you because your resume is going everywhere except the door that needs knocking?

**How is this different to sending a traditional email?** <br>
1. Generate emails instantly without writing them from scratch.
2. Choose the tone (formal, professional, friendly, celebratory) and preview the subject and body before sending.
3. Attach files, not only for extra context, but also send to multiple recipients in one streamlined workflow.

## Languages, Tools, and Technologies
- **Python** for programming
- **Gradio** for UI
- **OpenAI Agents SDK** for defining AI Agents<br>
(I used the gpt-4o-mini model across my agents, since none of my agents require heavy reasoning. It's cheap and a pretty lightweight model.)<br>
- **Pydantic** – Used for structured outputs and data validation between agents  
- **Code Editor / IDE** – VSCode or Cursor recommended for running and editing the project <br>
(Terminal / CLI Access – Required to install dependencies and run the project)

- **MailGun** – service for sending emails

## Estimated Cost

MailGun → I used the free tier of 100 emails/day. Upgrade as needed.<br>
OpenAI → as per usage and selection of models, my overall spend was <$1.

## Before you run your project...
1. Create an account on https://platform.openai.com/ and add in your credit card details for billing.
2. Generate an API key<br>
(If you want to use models from other LLM providers, you would want to do steps 1 and 2 for all of them)<br>
3. Create an account on https://login.mailgun.com/login/ (or any emailing service) to setup your credentials. Copy the API key and domain.<br>
(You can absolutely make things run with only setting up a verified email, but some email providers like Gmail do not authorize these emails, so you'll find the emails in spam. I used a verified custom domain)
4. Create a file in your project folder and name it `.env`
5. Copy-paste this block in it and fill it with your API keys:<br>
```
OPENAI_API_KEY="sk-proj-your-own-api-key"
ANTHROPIC_API_KEY="sk-ant-your-own-api-key" # optional, I created the client for you to mess around
GOOGLE_API_KEY="AIza-your-own-api-key" # optional, I created the client for you to mess around
MAILGUN_API_KEY="your-mailgun-api-key"
MAILGUN_DOMAIN="your-mailgun-domain"
SENDER_NAME="replace-with-your-display-name"
SENDER_EMAIL_ADDRESS="replace-with-your-email"
```

## Showtime
Run the following command in your terminal to execute the project:
```
./start.sh
```
**If you want to see what's behind the curtain…** <br>
You can look at your pipeline and agent responses at https://platform.openai.com/logs?api=traces<br><br>
**If you want to add new dependencies…** <br>
Like importing a new library, do this (similar to `npm install package_name`)

```bash
uv add package_name # ex: uv add pypdf
```
Then run your project as shown above.

## Future Work

- Testing responses with different kinds of LLM models
- Testing Agentic workflows as [suggested by Anthropic](https://www.anthropic.com/engineering/building-effective-agents#building-blocks-workflows-and-agents)
- CRUD operations on email list to add and remove specific emails
- Add bcc option to hide other recipients
- Allow images as attachments than just PDF; to send, or take context from
- Provide each user an account login, to save drafts and previously sent emails 


## Extra Info

I own a custom domain and verified it with Mailgun by configuring the required DNS records on my domain. This is supposed to ensure that the emails are properly authenticated and prevent them from being flagged as spam. (Sometimes my MailGun emails still get marked as spam, I'm open to suggestions as to how to totally avoid it from happening).

## End Credits

My tool is free to use and I welcome any improvements and criticism! Since this involves the use of AI agents (with multiple LLM calls) I would ask you to replace the API keys with your own to test it out on your own. All the instructions have been outlined. If you are not familiar with git or setting up projects on your computer, or you just want to skip the hassle because you can, I’m happy to connect and go over the app myself!
