from typing import Any

from google.adk.agents import llm_agent
from vertexai.preview.reasoning_engines import AdkApp
from google.adk.tools import agent_tool
from google.adk.tools.google_search_tool import GoogleSearchTool
from google.adk.tools import url_context


class AgentClass:

    def __init__(self):
        self.app = None

    def set_up(self):
        """Sets up the ADK application."""

        # Google Search Agent
        gap_discovery_agent_google_search_agent = llm_agent.LlmAgent(
            name='GAP_Discovery_Agent_google_search_agent',
            model='gemini-2.5-flash',
            description='Agent specialized in performing Google searches.',
            instruction='Use the GoogleSearchTool to find information on the web.',
            tools=[GoogleSearchTool()],
        )

        # URL Context Agent
        gap_discovery_agent_url_context_agent = llm_agent.LlmAgent(
            name='GAP_Discovery_Agent_url_context_agent',
            model='gemini-2.5-flash',
            description='Agent specialized in fetching content from URLs.',
            instruction='Use the UrlContextTool to retrieve content from provided URLs.',
            tools=[url_context],
        )

        # Main GAP Agent
        root_agent = llm_agent.LlmAgent(
            name='GAP_Discovery_Agent',
            model='gemini-2.5-flash',
            description='Helps users understand their strengths, gaps, and future direction.',
            instruction="""
Question Flow:

Ask the user questions across 4 areas:

1. Self-awareness (UIP)
- What are 2–3 things you are naturally good at? Give examples.
- What kind of activities make you lose track of time?

2. AI Understanding
- How do you think AI will impact your future career?
- Have you used any AI tools? What did you use them for?

3. Emotional Intelligence
- Tell me about a time you faced a challenge or failure. How did you handle it?
- How do you usually respond when someone disagrees with you?

4. Interdisciplinary Thinking
- Have you ever combined skills from different areas to solve a problem?
- How would you approach solving a real-world problem?

Rules:
- Ask ONE question at a time
- Do NOT skip areas

Evaluation Criteria:
1. Clarity
2. Depth
3. Evidence

Scoring:
Beginner / Developing / Strong

Final Output:
GAP Snapshot
Key Strengths
Key Gaps
Recommended Next Steps
""",
            tools=[
                agent_tool.AgentTool(agent=gap_discovery_agent_google_search_agent),
                agent_tool.AgentTool(agent=gap_discovery_agent_url_context_agent)
            ],
        )

        # IMPORTANT: No session_service_builder (fixes your error)
        self.app = AdkApp(
            agent=root_agent
        )

    async def stream_query(self, query: str, user_id: str = 'test') -> Any:
        async for chunk in self.app.async_stream_query(
            message=query,
            user_id=user_id,
        ):
            yield chunk


# Initialize properly
app = AgentClass()
app.set_up()