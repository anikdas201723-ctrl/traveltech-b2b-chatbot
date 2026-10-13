import streamlit as st
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Sriggle B2B Tech Support",
    page_icon="🛠️",
    layout="centered"
)

st.title("🛠️ Sriggle B2B Tech Support")
st.caption("24/7 AI-style technical support demo for travel platform partners")

st.info(
    "Demo project: answers are based on sample support scenarios. "
    "No real account, API key, webhook, billing system, or support desk is connected."
)

SCENARIOS = {
    "API & Integration — 401 Unauthorized": {
        "question": "We’re getting a 401 Unauthorized response code when attempting to call the Booking Engine API from our staging environment. How do we fix this?",
        "keywords": ["401", "unauthorized", "api", "authorization", "staging", "key", "integration"],
        "answer": """
**Likely cause**

A `401 Unauthorized` response commonly means the request is missing valid authentication credentials, or the credentials are expired or incorrect.

**Resolution steps**

1. In the sample platform, open **Admin Dashboard → Developer Settings → API Keys**.
2. Confirm the request includes an authorization header in the expected format:
   `Authorization: Bearer <YOUR_STAGING_API_KEY>`
3. Verify that you are using the staging key (for example, `sk_test_...`) rather than a production key (for example, `sk_live_...`).
4. If the key has expired, generate a replacement staging key and update the staging environment variable.
5. Retry the request and inspect the response.

**Security reminder:** never paste real API keys or passwords into this chatbot. Menu names and key prefixes above are illustrative and should be checked against your actual platform documentation.
""",
        "source": "Sample API Integration Guide"
    },
    "Account & Access — Password reset": {
        "question": "One of our new operations managers can't log in to the portal. She isn't receiving the password reset email.",
        "keywords": ["login", "log in", "password", "reset", "email", "invitation", "account", "access"],
        "answer": """
**Likely cause**

Password reset messages may be blocked by corporate spam filters, or the account may still be awaiting activation.

**Resolution steps**

1. Open **Settings → Team & Roles** in the sample admin panel.
2. Check whether the user is **Active** or **Pending Invitation**.
3. If pending, resend the invitation and ask the user to complete activation.
4. If active, check the Spam/Junk folder for messages from your platform's verified support address.
5. If corporate mail filtering is strict, ask your IT team to allow-list the platform's verified sending domain.

Do not allow-list a domain until your platform administrator has confirmed the correct sender domain. The menu names and sender address in this demo are examples.
""",
        "source": "Sample Account & Access Guide"
    },
    "Configuration — Cancellation policies": {
        "question": "How do we configure custom cancellation policies for different inventory types in the Booking Engine?",
        "keywords": ["configuration", "configure", "cancellation", "policy", "policies", "inventory", "booking engine", "refund"],
        "answer": """
**Likely cause**

Different inventory categories may need their own policy rules rather than one global default policy.

**Resolution steps**

1. Open **Booking Engine → Rules & Policies** in the sample platform.
2. Choose **Create Policy Overrides**.
3. Select the relevant inventory category, such as Premium or Standard.
4. Set the cancellation window and refund terms according to your business rules.
5. Assign the policy to the relevant inventory group.
6. Review the rules, then save and publish if you have the required permissions.

For example, a policy might allow a full refund up to 48 hours before arrival, but the actual terms must match your contract and product rules.

**Manual reference:** Booking Engine Admin Manual, page 14 (sample reference; no real manual is attached to this demo).
""",
        "source": "Sample Booking Engine Admin Manual"
    },
    "Performance — Webhook delays": {
        "question": "Our webhook notifications for completed bookings are failing or coming in with a 10-minute delay. What should we check?",
        "keywords": ["webhook", "delay", "delayed", "notifications", "completed bookings", "timeout", "5000", "200 ok", "performance"],
        "answer": """
**Likely cause**

Webhook delays can happen when the receiving endpoint is slow, unavailable, or returns an unsuccessful response. Retry queues can also contribute to delays.

**Resolution steps**

1. Inspect your receiver's server logs around the affected timestamps.
2. Make sure the endpoint acknowledges valid webhook requests promptly, using the status code required by your provider.
3. Move slow processing to a background job after safely recording the event.
4. In the sample portal, check **Developer Settings → Webhooks → Health Log** for failed deliveries, response codes, and retry attempts.
5. Test your endpoint using a tool such as Postman or Webhook.site.
6. Verify the provider's timeout and retry policy; the 5-second target in this example is not universal.

Do not share secret webhook signing keys or customer data in public logs.
""",
        "source": "Sample Webhook Troubleshooting Guide"
    },
    "Escalation — Billing sync affecting many accounts": {
        "question": "Our billing sync failed during midnight maintenance, and now 40 customer accounts are showing incorrect subscription statuses in our CRM.",
        "keywords": ["billing", "sync", "subscription", "crm", "accounts", "incorrect", "maintenance", "escalate", "urgent", "human", "ticket"],
        "answer": """
**High-priority escalation recommended**

Because this issue affects subscription status across multiple accounts and may affect billing operations, stop any risky manual bulk changes and escalate to your authorized billing or Level 2 technical support team.

**Information to include in the ticket**

- Approximate time and time zone of the failed sync
- Number of affected accounts (reported here as 40)
- Relevant job/run ID and sanitized error logs
- CRM and billing integration names
- Whether new billing or access changes are still running

**Demo ticket created**

- Ticket ID: `TK-DEMO-88392`
- Priority: High
- Status: Ready for human review
- Action: Escalation details prepared from the information in this example

**Important:** this is a simulated ticket for the college project. No real ticket was submitted, no logs were attached, and no specialist has been notified. Any response-time promise must come from the actual support team's SLA.
""",
        "source": "Sample Incident Escalation Procedure"
    }
}

def choose_scenario(message):
    text = message.lower()
    # Prioritize the most specific patterns first.
    if any(x in text for x in ["billing", "subscription status", "40 customer", "crm sync", "midnight maintenance"]):
        return "Escalation — Billing sync affecting many accounts"
    if any(x in text for x in ["webhook", "10-minute", "10 minute", "notification delay", "5000ms"]):
        return "Performance — Webhook delays"
    if any(x in text for x in ["cancellation", "inventory type", "policy override", "booking engine configuration"]):
        return "Configuration — Cancellation policies"
    if any(x in text for x in ["password reset", "can't log in", "cannot log in", "can't login", "invitation", "reset email"]):
        return "Account & Access — Password reset"
    if any(x in text for x in ["401", "unauthorized", "api key", "staging environment", "authorization header"]):
        return "API & Integration — 401 Unauthorized"
    # Use lightweight keyword matching for less exact phrasing.
    words = set(text.replace("?", " ").replace(",", " ").split())
    best_name, best_score = None, 0
    for name, item in SCENARIOS.items():
        score = sum(1 for keyword in item["keywords"] if keyword in text or keyword in words)
        if score > best_score:
            best_name, best_score = name, score
    return best_name if best_score >= 2 else None

if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "Hi! I'm the Sriggle B2B Tech Support Agent. Ask me about API errors, "
            "login and access, booking configuration, webhook delays, or billing incidents."
        ),
        "source": None
    }]

with st.sidebar:
    st.header("Quick questions")
    st.caption("Click a scenario to test the chatbot.")
    for name, item in SCENARIOS.items():
        if st.button(name, use_container_width=True):
            st.session_state.pending_question = item["question"]
    st.divider()
    st.caption("Prototype built with Python + Streamlit")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("source"):
            st.caption("Knowledge source: " + msg["source"])

prompt = st.chat_input("Describe your technical support issue...")

if "pending_question" in st.session_state:
    prompt = st.session_state.pop("pending_question")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
        "source": None
    })
    scenario_name = choose_scenario(prompt)

    if scenario_name:
        scenario = SCENARIOS[scenario_name]
        response = scenario["answer"]
        source = scenario["source"]
    else:
        response = (
            "I couldn't confidently match that question to the five sample support guides. "
            "Please try one of the quick questions, add more details such as the error code, "
            "or use the escalation form below. This demo doesn't have access to a real support system."
        )
        source = None

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "source": source
    })
    st.rerun()

st.divider()
st.subheader("🎫 Escalate to human support")
st.write("Use this demo form if the answer does not resolve the issue.")

with st.form("ticket_form"):
    contact = st.text_input("Work email (optional)")
    category = st.selectbox(
        "Issue category",
        ["API & Integration", "Account & Access", "Configuration",
         "Performance / Webhooks", "Billing / High priority", "Other"]
    )
    priority = st.selectbox("Priority", ["Normal", "High", "Critical"])
    details = st.text_area("Issue details (remove passwords, API keys, and customer-sensitive data)")
    submitted = st.form_submit_button("Create demo support ticket")

if submitted:
    if len(details.strip()) < 10:
        st.warning("Please provide at least 10 characters describing the issue.")
    else:
        ticket_id = "TK-" + uuid.uuid4().hex[:6].upper()
        st.success(
            f"Demo ticket **{ticket_id}** created in this session. "
            "It has not been sent to a real support team."
        )
        st.write(f"**Category:** {category} · **Priority:** {priority}")
        st.caption("For this prototype, ticket details are not sent externally or saved permanently.")
